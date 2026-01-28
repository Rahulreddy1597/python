import os
import re
import urllib.parse
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.set_page_config(page_title="Car Sales AI Assistant", layout="wide")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD_RAW = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("CLEANED_DB_NAME")
TABLE_NAME = os.getenv("CLEANED_TABLE_NAME")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY is not set in environment variables")
    st.stop()

if not DB_USER or DB_NAME is None or TABLE_NAME is None:
    st.error("DB_USER, CLEANED_DB_NAME, and CLEANED_TABLE_NAME must be set as environment variables")
    st.stop()

DB_PASSWORD = urllib.parse.quote_plus(DB_PASSWORD_RAW)

client = OpenAI(api_key=OPENAI_API_KEY)

def build_engine():
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url, pool_pre_ping=True)

engine = build_engine()

@st.cache_data(show_spinner=False)
def load_data():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    df = pd.read_sql(text(f"SELECT * FROM `{TABLE_NAME}`"), engine)

    if "sale_date" in df.columns:
        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
        df["sale_year"] = df["sale_date"].dt.year
    elif "sale_year" not in df.columns:
        df["sale_year"] = pd.NA

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Database connection or read failed: {e}")
    st.stop()

MARKET_ALIASES = {
    "dfw": "Dallas–Fort Worth",
    "dallas": "Dallas–Fort Worth",
    "dallas fort worth": "Dallas–Fort Worth",
    "los angeles": "Los Angeles",
    "la": "Los Angeles",
    "san juan": "San Juan",
}

def parse_year_and_market(question: str):
    q = (question or "").lower()

    year = None
    m = re.search(r"\b(20\d{2})\b", q)
    if m:
        year = int(m.group(1))

    market = None
    for k, v in MARKET_ALIASES.items():
        if k in q:
            market = v
            break

    return year, market

def compute_top_models_slice(df_in: pd.DataFrame, year: int | None, market: str | None, top_n: int = 12):
    if df_in is None or df_in.empty:
        return pd.DataFrame()

    d = df_in.copy()

    if year is not None:
        if "sale_year" not in d.columns:
            if "sale_date" in d.columns:
                d["sale_date"] = pd.to_datetime(d["sale_date"], errors="coerce")
                d["sale_year"] = d["sale_date"].dt.year
            else:
                return pd.DataFrame()
        d = d[d["sale_year"] == year]

    if market is not None and "market" in d.columns:
        d = d[d["market"] == market]

    if d.empty:
        return pd.DataFrame()

    agg = (
        d.groupby(["market", "make", "model"], as_index=False)
        .agg(units_sold=("sale_id", "count"), avg_price=("price", "mean"))
        .sort_values("units_sold", ascending=False)
        .head(top_n)
    )

    agg["avg_price"] = agg["avg_price"].fillna(0.0)
    return agg

def slice_to_text(agg: pd.DataFrame, year: int | None, market: str | None):
    if agg is None or agg.empty:
        return f"No rows match filters year={year}, market={market}."

    lines = []
    for _, r in agg.iterrows():
        units = int(r.get("units_sold", 0))
        avgp = float(r.get("avg_price", 0.0))
        lines.append(f"{r['market']} | {r['make']} {r['model']} | units_sold={units} | avg_price={avgp:.0f}")
    return "\n".join(lines)

st.title("AI Car Sales and Inventory Assistant")
st.markdown(
    """
This assistant answers dealership questions using your **actual database data** (not guesses).
Ask questions like:

- Best selling models in 2024, DFW area
- Top models in Los Angeles in 2021
- Which market has the highest average price in 2025
"""
)

st.subheader("Suggested Questions")

suggested_questions = [
    "Best selling models in 2024, DFW area",
    "Top selling models in 2025, Los Angeles",
    "Which market has the highest average vehicle price in 2024",
    "What were the top selling models in San Juan in 2023",
]

cols = st.columns(2)
for i, q in enumerate(suggested_questions):
    if cols[i % 2].button(q):
        st.session_state["question_prefill"] = q

if "messages" not in st.session_state:
    st.session_state.messages = []

user_question = st.text_input(
    "Ask a question about sales, buyers, or inventory",
    value=st.session_state.get("question_prefill", "")
)

def build_system_prompt(data_context_text: str):
    return f"""
You are a dealership analytics assistant.

Rules
- Answer only using the data context I provide below.
- If the question asks for a slice such as year or market, use ONLY that slice.
- If the slice is empty, say exactly which filters were applied and that no rows matched.
- Be concise and executive friendly.
- Do not ask the user to run SQL.

Dataset context
- Data covers sale years derived from sale_date (2015 to 2025).
- Columns include sale_id, sale_date, sale_year, market, make, model, model_year, price,
  buyer_age, buyer_age_group, buyer_income_bracket, purchase_type.

Precomputed slice for this question (top models and avg price)
{data_context_text}
"""

if st.button("Ask AI") and user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})

    year, market = parse_year_and_market(user_question)
    agg = compute_top_models_slice(df, year=year, market=market, top_n=12)
    data_context_text = slice_to_text(agg, year=year, market=market)

    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {"role": "system", "content": build_system_prompt(data_context_text)},
            *st.session_state.messages,
        ],
    )

    answer = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})

st.subheader("Conversation")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")

st.subheader("What the AI used for the last answer")

if st.session_state.messages:
    last_user = None
    for m in reversed(st.session_state.messages):
        if m["role"] == "user":
            last_user = m["content"]
            break

    if last_user:
        year, market = parse_year_and_market(last_user)
        agg = compute_top_models_slice(df, year=year, market=market, top_n=20)
        if agg.empty:
            st.write(f"No rows matched year={year}, market={market}.")
        else:
            st.dataframe(agg, use_container_width=True)

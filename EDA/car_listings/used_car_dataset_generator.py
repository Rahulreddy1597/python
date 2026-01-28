import os
import re
import urllib.parse
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from openai import OpenAI


st.set_page_config(page_title="Car Sales AI Assistant", layout="wide")


DB_USER = os.getenv("DB_USER")
DB_PASSWORD_RAW = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("CLEANED_DB_NAME")
TABLE_NAME = os.getenv("CLEANED_TABLE_NAME")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY is not set in environment variables")
    st.stop()

if not DB_USER or not DB_HOST or not DB_PORT or not DB_NAME or not TABLE_NAME:
    st.error("Missing DB env vars. Need DB_USER, DB_HOST, DB_PORT, CLEANED_DB_NAME, CLEANED_TABLE_NAME.")
    st.stop()


def safe_quote(s):
    if s is None:
        return ""
    return urllib.parse.quote_plus(str(s))


DB_PASSWORD = safe_quote(DB_PASSWORD_RAW)

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True,
)

client = OpenAI(api_key=OPENAI_API_KEY)


def normalize_text(v):
    if v is None:
        return ""
    s = str(v).strip().lower()
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^a-z0-9 \-]", "", s)
    return s


MARKET_ALIASES_NORM = {
    "dfw": "dallas-fort worth",
    "dallas": "dallas-fort worth",
    "dallas fort worth": "dallas-fort worth",
    "dallas-fort worth": "dallas-fort worth",
    "los angeles": "los angeles",
    "la": "los angeles",
    "san juan": "san juan",
}


@st.cache_data(show_spinner=False)
def load_data():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    df = pd.read_sql(text(f"SELECT * FROM `{TABLE_NAME}`"), engine)

    if "sale_date" in df.columns:
        df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
        df["sale_year"] = df["sale_date"].dt.year
    elif "sale_year" in df.columns:
        df["sale_year"] = pd.to_numeric(df["sale_year"], errors="coerce")
    else:
        df["sale_year"] = pd.NA

    if "market" in df.columns:
        df["market_norm"] = df["market"].apply(normalize_text)
    else:
        df["market_norm"] = ""

    return df


def parse_year_and_market(question):
    q = normalize_text(question)

    year = None
    m = re.search(r"\b(20\d{2})\b", q)
    if m:
        year = int(m.group(1))

    market_norm = None
    for k, v in MARKET_ALIASES_NORM.items():
        if k in q:
            market_norm = v
            break

    return year, market_norm


def slice_top_models(df_all, year, market_norm, top_n):
    d = df_all.copy()

    if year is not None:
        d = d[d["sale_year"] == year]

    if market_norm is not None:
        d = d[d["market_norm"] == market_norm]

    if d.empty:
        return pd.DataFrame()

    if "make" not in d.columns or "model" not in d.columns:
        return pd.DataFrame()

    agg = (
        d.groupby(["market", "make", "model"], as_index=False)
        .agg(units_sold=("sale_id", "count"), avg_price=("price", "mean"))
        .sort_values("units_sold", ascending=False)
        .head(top_n)
    )

    agg["avg_price"] = agg["avg_price"].fillna(0.0)
    return agg


def df_to_compact_lines(df_in):
    if df_in is None or df_in.empty:
        return "No rows in this slice."
    lines = []
    for _, r in df_in.iterrows():
        units = int(r.get("units_sold", 0))
        avgp = float(r.get("avg_price", 0.0))
        lines.append(f"{r['market']} | {r['make']} {r['model']} | units_sold={units} | avg_price={avgp:.0f}")
    return "\n".join(lines)


def build_system_prompt(table_name, years_min, years_max, slice_text, year, market_norm, market_examples):
    return f"""
You are a dealership analytics assistant.

Rules
- Answer only using the data slice I provide.
- If the user asks for a specific year or market, use only that slice.
- If the slice is empty, say the filters applied and suggest the closest valid market values from the dataset.
- Keep the answer executive friendly and direct.
- Do not ask the user to run SQL.

Data details
- Source table: {table_name}
- Sale years available: {years_min} to {years_max}
- Market examples in data: {market_examples}

Filters applied
- sale_year: {year}
- market: {market_norm}

Slice (top models and avg price)
{slice_text}
"""


st.title("Car Sales AI Assistant")
st.markdown(
    """
Ask questions like:
- Best selling models in 2024, DFW area
- Top selling models in 2022, Los Angeles
- What are the top models in San Juan in 2025
"""
)


try:
    df = load_data()
except Exception as e:
    st.error(f"Database connection or read failed: {e}")
    st.stop()


with st.expander("Debug dataset coverage", expanded=False):
    st.write("Row count:", int(len(df)))
    if "sale_year" in df.columns:
        st.write("Sale years min max:", df["sale_year"].min(), df["sale_year"].max())
        year_counts = df["sale_year"].value_counts(dropna=False).sort_index()
        st.write("Sale year counts (first 15):")
        st.dataframe(year_counts.head(15))
    if "market" in df.columns:
        mk = df["market"].value_counts().head(10).reset_index()
        mk.columns = ["market_value", "rows"]
        st.write("Top market values in data:")
        st.dataframe(mk)

st.subheader("Suggested questions")
suggested = [
    "Best selling models in 2022, DFW area",
    "Best selling models in 2024, DFW area",
    "Top selling models in 2023, Los Angeles",
    "Top selling models in 2025, San Juan",
]
c1, c2 = st.columns(2)
for i, q in enumerate(suggested):
    if (c1 if i % 2 == 0 else c2).button(q):
        st.session_state["prefill"] = q

if "messages" not in st.session_state:
    st.session_state.messages = []

user_question = st.text_input("Ask a question", value=st.session_state.get("prefill", ""))

if st.button("Ask AI") and user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})

    year, market_norm = parse_year_and_market(user_question)

    agg = slice_top_models(df, year=year, market_norm=market_norm, top_n=12)
    slice_text = df_to_compact_lines(agg)

    years_min = df["sale_year"].min() if "sale_year" in df.columns else None
    years_max = df["sale_year"].max() if "sale_year" in df.columns else None

    market_examples = ", ".join(df["market"].dropna().astype(str).value_counts().head(5).index.tolist()) if "market" in df.columns else ""

    system_prompt = build_system_prompt(
        table_name=TABLE_NAME,
        years_min=years_min,
        years_max=years_max,
        slice_text=slice_text,
        year=year,
        market_norm=market_norm,
        market_examples=market_examples,
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages,
        ],
    )

    answer = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})


st.subheader("Conversation")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown("You: " + msg["content"])
    else:
        st.markdown("AI: " + msg["content"])


st.subheader("Last slice used")
last_user = None
for m in reversed(st.session_state.messages):
    if m["role"] == "user":
        last_user = m["content"]
        break

if last_user:
    year, market_norm = parse_year_and_market(last_user)
    agg = slice_top_models(df, year=year, market_norm=market_norm, top_n=20)
    if agg.empty:
        st.write("No rows matched. Check Debug dataset coverage to confirm market values and years exist.")
    else:
        st.dataframe(agg, use_container_width=True)

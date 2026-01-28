import os
import urllib.parse
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

# -------------------- Load Environment --------------------
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("CLEANED_DB_NAME")
TABLE_NAME = os.getenv("CLEANED_TABLE_NAME")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -------------------- Load Data --------------------
@st.cache_data
def load_data():
    df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", engine)
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df["sale_year"] = df["sale_date"].dt.year
    return df

df = load_data()

# -------------------- Dashboard Header --------------------
st.title("Automotive Sales & Inventory Dashboard")
st.markdown(
    """
    This dashboard provides insights into historical vehicle sales from 2015 to 2025, 
    buyer demographics, sales trends, and inventory recommendations. 
    Use the sidebar filters to explore data by market, make, model, and sale year.
    The inventory recommendations are based on overall sales trends and are not affected by sidebar filters.
    """
)
st.markdown("---") 

# -------------------- Sidebar Filters --------------------
st.sidebar.header("Filters")

# Market filter (empty by default)
markets = df["market"].sort_values().unique()
selected_market = st.sidebar.selectbox("Select Market (optional)", ["All"] + list(markets), index=0)

# Make filter (depends on selected market)
if selected_market != "All":
    makes = df[df["market"] == selected_market]["make"].sort_values().unique()
else:
    makes = df["make"].sort_values().unique()
selected_make = st.sidebar.selectbox("Select Make (optional)", ["All"] + list(makes), index=0)

# Model filter (depends on make)
if selected_make != "All":
    models = df[df["make"] == selected_make]["model"].sort_values().unique()
else:
    models = df["model"].sort_values().unique()
selected_model = st.sidebar.selectbox("Select Model (optional)", ["All"] + list(models), index=0)

# Year filter
years = df["sale_year"].sort_values().unique()
selected_year = st.sidebar.selectbox("Select Sale Year (optional)", ["All"] + list(years), index=0)

# -------------------- Filter Data --------------------
df_filtered = df.copy()

if selected_market != "All":
    df_filtered = df_filtered[df_filtered["market"] == selected_market]
if selected_make != "All":
    df_filtered = df_filtered[df_filtered["make"] == selected_make]
if selected_model != "All":
    df_filtered = df_filtered[df_filtered["model"] == selected_model]
if selected_year != "All":
    df_filtered = df_filtered[df_filtered["sale_year"] == selected_year]

# -------------------- KPIs --------------------
st.subheader("Key Performance Indicators (KPIs)")
st.markdown(
    "Summary of sales metrics. Average units sold per year, average price, and best performing model "
    "based on total sales, considering the current sidebar filters."
)

df_kpi = df_filtered.copy()  # respects sidebar filters
years_count = df_kpi['sale_date'].dt.year.nunique()

avg_units_per_year = df_kpi.groupby('sale_date').size().sum() / max(years_count, 1)
avg_price = df_kpi['price'].mean()

# Best performing model
best_model_row = df_kpi.groupby(['make', 'model']).agg(total_units=('sale_id', 'count')).reset_index()
best_model_row = best_model_row.sort_values('total_units', ascending=False).iloc[0]

# Helper function to dynamically resize text for KPI
def kpi_html(title, value, max_length=25):
    """Dynamically adjust font size based on length of value string."""
    base_size = 28
    length = len(value)
    if length > max_length:
        size = max(base_size - (length - max_length) * 1.2, 12)
    else:
        size = base_size
    html = f"""
    <div style="text-align:center; margin-bottom:10px;">
        <div style="font-size:16px; color:gray;">{title}</div>
        <div style="font-size:{size}px; font-weight:bold;">{value}</div>
    </div>
    """
    return html

col1, col2, col3 = st.columns(3)

col1.markdown(kpi_html("Avg Units Sold per Year", f"{avg_units_per_year:.0f}"), unsafe_allow_html=True)
col2.markdown(kpi_html("Average Price", f"${avg_price:,.0f}"), unsafe_allow_html=True)
col3.markdown(
    kpi_html(
        "Best Performing Model",
        f"{best_model_row['make']} {best_model_row['model']} ({best_model_row['total_units']} units)"
    ),
    unsafe_allow_html=True
)

# -------------------- Historical Sales --------------------
st.subheader("Historical Sales Data")
st.markdown(
    "Table showing sales data by model year, make, and model. "
    "Use the filters to inspect historical performance for specific markets, makes, models, and years."
)

# Year filter for visualization (optional, respects sidebar selections)
year_options = sorted(df_filtered['sale_date'].dt.year.unique())
selected_year = st.selectbox("Filter by Sale Year (optional)", options=[None] + year_options, index=0)

df_hist = df_filtered.copy()
if selected_year:
    df_hist = df_hist[df_hist['sale_date'].dt.year == selected_year]

# Aggregate for table
df_hist_agg = df_hist.groupby(
    ["model_year", "make", "model"]
).agg(
    units_sold=("sale_id", "count"),
    avg_buyer_age=("buyer_age", "mean"),
    avg_price=("price", "mean")
).reset_index()

st.dataframe(df_hist_agg.sort_values(["model_year", "units_sold"], ascending=[False, False]))

# -------------------- Buyer Demographics --------------------
st.subheader("Buyer Demographics")
st.markdown("Distribution of buyer age groups and income brackets for selected filters.")

if not df_filtered.empty:
    fig_age = px.histogram(
        df_filtered,
        x="buyer_age_group",
        color="buyer_age_group",
        title="Buyer Age Group Distribution",
        labels={"buyer_age_group": "Age Group"},
        text_auto=True
    )
    st.plotly_chart(fig_age, use_container_width=True)

    fig_income = px.histogram(
        df_filtered,
        x="buyer_income_bracket",
        color="buyer_income_bracket",
        title="Buyer Income Bracket Distribution",
        labels={"buyer_income_bracket": "Income Bracket"},
        text_auto=True
    )
    st.plotly_chart(fig_income, use_container_width=True)

# -------------------- Trend Visualizations --------------------
st.subheader("Sales Trend Over Years")
st.markdown("Shows how sales have changed over time for the selected filters.")

if not df_filtered.empty:
    df_trend = df_filtered.groupby("sale_year").agg(
        units_sold=("sale_id", "count"),
        avg_price=("price", "mean")
    ).reset_index()

    fig_trend_units = px.line(df_trend, x="sale_year", y="units_sold", title="Units Sold Over Years")
    st.plotly_chart(fig_trend_units, use_container_width=True)

# -------------------- Inventory Recommendation --------------------
st.subheader("Inventory Recommendations")
st.markdown(
    "Suggested inventory allocation across all markets, makes, and models. Percentages capped at 100%. "
    "This uses the full dataset and is **not affected** by sidebar filters."
)

# Aggregate units sold for all models
df_inv = df.groupby(["make", "model"]).agg(
    units_sold=("sale_id", "count")
).reset_index()

# Calculate percentage allocation
df_inv["percentage"] = 100 * df_inv["units_sold"] / df_inv["units_sold"].sum()

# Sort descending for best-selling to worst-selling
df_inv_sorted = df_inv.sort_values("percentage", ascending=False)

# -------------------- Horizontal Bar Chart --------------------
df_inv_sorted = df_inv.sort_values("percentage", ascending=True)

fig_inv_bar = px.bar(
    df_inv_sorted,
    x="percentage",
    y="model",
    orientation="h",
    color="make",
    hover_data=["make", "units_sold"],
    text=df_inv_sorted["percentage"].apply(lambda x: f"{x:.1f}%"),
    labels={"percentage": "Inventory %", "model": "Model"},
    height=max(400, 30 * len(df_inv_sorted)),  # dynamic height based on number of models
)

fig_inv_bar.update_layout(
    yaxis=dict(
        categoryorder="total ascending",  # best-selling on top
        automargin=True  # allows long model names to fit
    ),
    xaxis=dict(title="Inventory %"),
    margin=dict(l=200, r=50, t=50, b=50),  # increased left margin for long names
    title_text="Inventory Recommendations by Model (Horizontal Bar Chart)",
    title_x=0.5
)

st.plotly_chart(fig_inv_bar, use_container_width=True)

# -------------------- Optional Pie Chart (Commented Out) --------------------
# """
# fig_inv_pie = px.pie(
#     df_inv_sorted,
#     names="model",
#     values="percentage",
#     color="make",
#     title="Inventory Recommendations (Pie Chart)",
# )
# # st.plotly_chart(fig_inv_pie, use_container_width=True)
# """
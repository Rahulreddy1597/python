# train_model.py
import os
import urllib.parse
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sklearn.preprocessing import OneHotEncoder
import xgboost as xgb
import joblib

# -------------------------
# Load environment
# -------------------------
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("CLEANED_DB_NAME")
TABLE = os.getenv("CLEANED_TABLE_NAME")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -------------------------
# Load data
# -------------------------
df = pd.read_sql(f"SELECT * FROM {TABLE}", engine)

# Defensive checks (fail fast, clear error)
required_cols = {
    "sale_id",
    "sale_date",
    "market",
    "make",
    "model",
    "price",
    "buyer_annual_income",
}

missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {missing}")

df["sale_year"] = pd.to_datetime(df["sale_date"]).dt.year

# -------------------------
# Aggregate sales
# -------------------------
df_agg = (
    df.groupby(["market", "sale_year", "make", "model"])
    .agg(
        units_sold=("sale_id", "count"),
        avg_price=("price", "mean"),
        avg_buyer_income=("buyer_annual_income", "mean"),
    )
    .reset_index()
)

# -------------------------
# Convert to inventory percentage (target)
# -------------------------
df_agg["market_year_total"] = df_agg.groupby(
    ["market", "sale_year"]
)["units_sold"].transform("sum")

df_agg["inventory_pct"] = (
    df_agg["units_sold"] / df_agg["market_year_total"]
)

# -------------------------
# Feature prep
# -------------------------
categorical_features = ["market", "make", "model"]
numeric_features = ["sale_year", "avg_price", "avg_buyer_income"]

encoder = OneHotEncoder(
    sparse_output=False,
    handle_unknown="ignore"
)

X_cat = encoder.fit_transform(df_agg[categorical_features])
X_num = df_agg[numeric_features].fillna(0).values

X = np.hstack([X_num, X_cat])
y = df_agg["inventory_pct"].values

# -------------------------
# Train model
# -------------------------
model = xgb.XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="reg:squarederror",
    random_state=42,
)

model.fit(X, y)

# -------------------------
# Save artifacts
# -------------------------
joblib.dump(model, "inventory_model_pct.joblib")
joblib.dump(encoder, "inventory_encoder.joblib")

print("Training complete")
print("Saved inventory_model_pct.joblib")
print("Saved inventory_encoder.joblib")

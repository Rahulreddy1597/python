import os
import time
import pandas as pd
import numpy as np
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

def get_env(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing environment variable {name}")
    return value

DB_HOST = get_env("DB_HOST")
DB_PORT = get_env("DB_PORT")
DB_USER = quote_plus(get_env("DB_USER"))
DB_PASSWORD = quote_plus(get_env("DB_PASSWORD"))

CLEAN_DB = get_env("CLEANED_DB_NAME")
CLEAN_TABLE = get_env("CLEANED_TABLE_NAME")

FEATURE_DB = get_env("FEATURE_DB_NAME")
FEATURE_TABLE = get_env("FEATURE_TABLE_NAME")

BASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"

def connect_with_retry(db_name=None, retries=5, wait=3):
    url = BASE_URL if not db_name else f"{BASE_URL}/{db_name}"
    for attempt in range(1, retries + 1):
        try:
            engine = create_engine(url, pool_pre_ping=True)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"Connected to {db_name if db_name else 'server'} on attempt {attempt}")
            return engine
        except OperationalError as e:
            print(f"Connection failed on attempt {attempt}")
            print(str(e))
            time.sleep(wait)
    raise RuntimeError("Database connection failed")

print("Connecting to cleaned database")
clean_engine = connect_with_retry(CLEAN_DB)

print("Reading cleaned data")
df = pd.read_sql(f"SELECT * FROM {CLEAN_TABLE}", clean_engine)
print(f"Rows loaded {len(df)}")

print("Starting feature engineering")

# Price log transform
if "price" in df.columns:
    df["price_log"] = np.where(
        df["price"].notna() & (df["price"] > 0),
        np.log1p(df["price"]),
        None
    )

# Vehicle age
if "year" in df.columns:
    current_year = pd.Timestamp.now().year
    df["vehicle_age"] = current_year - df["year"]

# Market price comparison
if "market" in df.columns and "price" in df.columns:
    market_avg = df.groupby("market")["price"].transform("mean")
    df["market_avg_price"] = market_avg
    df["price_vs_market"] = df["price"] / market_avg

# Brand popularity
if "brand" in df.columns:
    brand_counts = df["brand"].value_counts()
    df["brand_popularity"] = df["brand"].map(brand_counts)

# Mileage buckets
if "mileage" in df.columns:
    df["mileage_bucket"] = pd.cut(
        df["mileage"],
        bins=[0, 25000, 50000, 100000, 200000, float("inf")],
        labels=["low", "medium", "high", "very_high", "extreme"]
    )

print("Feature engineering completed")
print("Feature columns:")
print(df.columns.tolist())

print("Ensuring feature database exists")
server_engine = connect_with_retry()
with server_engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {FEATURE_DB}"))

print("Connecting to feature database")
feature_engine = connect_with_retry(FEATURE_DB)

print("Writing feature table")
df.to_sql(
    FEATURE_TABLE,
    feature_engine,
    if_exists="replace",
    index=False,
    chunksize=1000
)

print("Feature store write completed")
print(f"Feature DB {FEATURE_DB}")
print(f"Feature table {FEATURE_TABLE}")
print(f"Total rows written {len(df)}")

print("Feature engineering pipeline finished successfully")

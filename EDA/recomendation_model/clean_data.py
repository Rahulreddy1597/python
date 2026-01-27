# clean_data.py
import os
import time
import pandas as pd
import urllib.parse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()  # Make sure you have a .env file in the same folder

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 3306)
DB_NAME = os.getenv("DB_NAME", "car_sales")
CLEAN_SCHEMA = os.getenv("CLEAN_SCHEMA", "car_sales_cleaned")

if not DB_USER or not DB_PASSWORD:
    raise ValueError("Database username or password not set in .env")

# URL encode password to handle special characters
DB_PASSWORD_ENC = urllib.parse.quote_plus(DB_PASSWORD)

# ------------------------------
# Retry connection logic
# ------------------------------
MAX_RETRIES = 3
SLEEP_SECONDS = 5
engine = None

for attempt in range(1, MAX_RETRIES + 1):
    try:
        engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD_ENC}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
            echo=False
        )
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"Connected to database {DB_NAME} on attempt {attempt}")
        break
    except Exception as e:
        print(f"Connection failed (attempt {attempt}): {e}")
        if attempt < MAX_RETRIES:
            print(f"Retrying in {SLEEP_SECONDS} seconds...")
            time.sleep(SLEEP_SECONDS)
        else:
            raise SystemExit("Maximum connection attempts reached. Exiting.")

# ------------------------------
# Create separate schema for cleaned data
# ------------------------------
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{CLEAN_SCHEMA}`"))
    print(f"Cleaned schema {CLEAN_SCHEMA} ready")

# ------------------------------
# Read raw data from original table
# ------------------------------
RAW_TABLE = "car_sales"  # original table name

try:
    df = pd.read_sql_table(RAW_TABLE, con=engine)
    print(f"Loaded {len(df)} rows from table {RAW_TABLE}")
except Exception as e:
    raise SystemExit(f"Error reading from table {RAW_TABLE}: {e}")

# ------------------------------
# Data Cleaning
# ------------------------------
print("Cleaning data...")

# Example cleaning steps
df.drop_duplicates(subset="sale_id", inplace=True)
df['buyer_annual_income'] = df.groupby('market')['buyer_annual_income'].transform(
    lambda x: x.fillna(x.median())
)
df['payment_to_income_ratio'] = df.groupby('purchase_type')['payment_to_income_ratio'].transform(
    lambda x: x.fillna(x.median())
)

# ------------------------------
# Upload cleaned data to new schema
# ------------------------------
CLEAN_TABLE = "car_sales_cleaned"

with engine.connect() as conn:
    conn.execute(text(f"USE `{CLEAN_SCHEMA}`"))

try:
    df.to_sql(
        CLEAN_TABLE,
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=5000
    )
    print(f"Cleaned data uploaded to {CLEAN_SCHEMA}.{CLEAN_TABLE} successfully!")
except Exception as e:
    raise SystemExit(f"Error uploading cleaned data: {e}")

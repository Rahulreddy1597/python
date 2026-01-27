# db_data_loader.py

import time
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError
from getpass import getpass  # For hidden password input

# -----------------------------
# Step 1: Get DB details from user
# -----------------------------
DB_USER = input("Enter MySQL username: ")
DB_PASSWORD = getpass("Enter MySQL password (hidden): ")
DB_HOST = input("Enter MySQL host (default: localhost): ") or "localhost"
DB_PORT = input("Enter MySQL port (default: 3306): ") or 3306
DB_NAME = input("Enter database name to create/use: ")

CSV_FILE = input("Enter path to CSV file (default: car_sales_data.csv): ") or "car_sales_data.csv"
TABLE_NAME = "car_sales"

# -----------------------------
# Step 2: Build SQLAlchemy engine safely
# -----------------------------
def create_mysql_engine(user, password, host, port, database=None):
    url = URL.create(
        drivername="mysql+pymysql",
        username=user,
        password=password,
        host=host,
        port=int(port),
        database=database
    )
    return create_engine(url, pool_pre_ping=True, echo=False)

# Engine to connect to server (without database yet)
server_engine = create_mysql_engine(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

# -----------------------------
# Step 3: Retry connection logic
# -----------------------------
MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds

for attempt in range(1, MAX_RETRIES + 1):
    try:
        with server_engine.connect() as conn:
            print(f"[✔] Connection successful on attempt {attempt}")
            # Wrap raw SQL in text()
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"))
            print(f"[✔] Database `{DB_NAME}` ready")
        break
    except OperationalError as e:
        print(f"[!] Connection attempt {attempt} failed: {e}")
        if attempt < MAX_RETRIES:
            print(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
        else:
            raise e

# -----------------------------
# Step 4: Connect to the specific database
# -----------------------------
db_engine = create_mysql_engine(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
print(f"[✔] Connected to database `{DB_NAME}` successfully!")

# -----------------------------
# Step 5: Upload CSV to MySQL
# -----------------------------
try:
    print(f"[...] Reading CSV file: {CSV_FILE}")
    df = pd.read_csv(CSV_FILE, parse_dates=['sale_date'])
    print(f"[✔] CSV loaded. {len(df)} rows found.")

    print(f"[...] Uploading data to MySQL table `{TABLE_NAME}` (if exists, it will be replaced)")
    df.to_sql(TABLE_NAME, db_engine, if_exists="replace", index=False)
    print(f"[✔] Data uploaded successfully to `{TABLE_NAME}` in database `{DB_NAME}`")

except FileNotFoundError:
    print(f"[✖] CSV file not found: {CSV_FILE}")
except Exception as e:
    print(f"[✖] Error uploading CSV: {e}")

# -----------------------------
# Step 6: Test reading back
# -----------------------------
try:
    print(f"[...] Testing read from MySQL table `{TABLE_NAME}`")
    test_df = pd.read_sql(f"SELECT * FROM {TABLE_NAME} LIMIT 5", db_engine)
    print("[✔] Test read successful:")
    print(test_df)
except Exception as e:
    print(f"[✖] Error reading from database: {e}")

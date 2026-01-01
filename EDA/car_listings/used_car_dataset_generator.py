import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ============================================================
# CONFIG
# ============================================================
N_ROWS = 500_000
np.random.seed(42)
random.seed(42)

# ============================================================
# MARKETS & GEO
# ============================================================
cities = {
    "Los Angeles": {
        "state": "CA",
        "zips": ["90001","90002","90003","90004","90005","90006","90007","90008","90010",
                 "90011","90012","90013","90014","90015","90016","90017","90018","90019",
                 "90020","90021"]
    },
    "Dallas": {
        "state": "TX",
        "zips": ["75201","75202","75203","75204","75205","75206","75207","75208","75209",
                 "75210","75211","75212","75214","75215","75216","75217","75218","75219"]
    },
    "Columbus": {
        "state": "OH",
        "zips": ["43004","43016","43026","43081","43085","43110","43201","43202","43203",
                 "43204","43205","43206","43207","43209","43211","43212","43213","43214"]
    }
}

market_weights = {"Los Angeles": 0.4, "Dallas": 0.35, "Columbus": 0.25}
markets = list(market_weights.keys())
market_prob = [market_weights[m] for m in markets]

# ============================================================
# BRANDS, MODELS, BODY TYPES
# ============================================================
brand_models = {
    "Toyota": [("Camry","Sedan"),("Corolla","Sedan"),("RAV4","SUV"),("Highlander","SUV"),("Tacoma","Truck"),("Prius","Hatchback")],
    "Honda": [("Civic","Sedan"),("Accord","Sedan"),("CR-V","SUV"),("Pilot","SUV"),("Fit","Hatchback")],
    "Ford": [("F-150","Truck"),("Explorer","SUV"),("Escape","SUV"),("Fusion","Sedan"),("Mustang","Coupe"),("Edge","SUV")],
    "Chevrolet": [("Silverado 1500","Truck"),("Equinox","SUV"),("Malibu","Sedan"),("Tahoe","SUV"),("Camaro","Coupe"),("Traverse","SUV")],
    "Nissan": [("Altima","Sedan"),("Sentra","Sedan"),("Rogue","SUV"),("Pathfinder","SUV"),("Frontier","Truck")],
    "Hyundai": [("Elantra","Sedan"),("Sonata","Sedan"),("Tucson","SUV"),("Santa Fe","SUV"),("Kona","SUV"),("Ioniq 5","SUV")],
    "Kia": [("Optima","Sedan"),("Forte","Sedan"),("Soul","Hatchback"),("Sportage","SUV"),("Sorento","SUV"),("EV6","SUV")],
    "Volkswagen": [("Jetta","Sedan"),("Passat","Sedan"),("Golf","Hatchback"),("Tiguan","SUV"),("Atlas","SUV")],
    "Subaru": [("Impreza","Hatchback"),("Legacy","Sedan"),("Outback","SUV"),("Forester","SUV"),("Crosstrek","SUV")],
    "Mazda": [("Mazda3","Sedan"),("Mazda6","Sedan"),("CX-3","SUV"),("CX-5","SUV"),("CX-9","SUV")],
    "Jeep": [("Wrangler","SUV"),("Grand Cherokee","SUV"),("Compass","SUV"),("Cherokee","SUV"),("Renegade","SUV")],
    "Dodge": [("Charger","Sedan"),("Challenger","Coupe"),("Durango","SUV"),("Journey","SUV")],
    "Ram": [("1500","Truck"),("2500","Truck"),("3500","Truck")],
    "GMC": [("Sierra 1500","Truck"),("Canyon","Truck"),("Terrain","SUV"),("Acadia","SUV"),("Yukon","SUV")],
    "Buick": [("Encore","SUV"),("Enclave","SUV"),("LaCrosse","Sedan")],
    "Chrysler": [("300","Sedan"),("Pacifica","Van")],
    "Mitsubishi": [("Outlander","SUV"),("Eclipse Cross","SUV"),("Mirage","Hatchback")],
    "BMW": [("3 Series","Sedan"),("5 Series","Sedan"),("X1","SUV"),("X3","SUV"),("X5","SUV"),("X7","SUV")],
    "Mercedes-Benz": [("C-Class","Sedan"),("E-Class","Sedan"),("GLC","SUV"),("GLE","SUV"),("GLS","SUV"),("A-Class","Sedan")],
    "Audi": [("A3","Sedan"),("A4","Sedan"),("A6","Sedan"),("Q3","SUV"),("Q5","SUV"),("Q7","SUV")],
    "Lexus": [("IS","Sedan"),("ES","Sedan"),("RX","SUV"),("NX","SUV"),("GX","SUV")],
    "Acura": [("ILX","Sedan"),("TLX","Sedan"),("RDX","SUV"),("MDX","SUV")],
    "Infiniti": [("Q50","Sedan"),("Q60","Coupe"),("QX50","SUV"),("QX60","SUV"),("QX80","SUV")],
    "Volvo": [("S60","Sedan"),("S90","Sedan"),("XC40","SUV"),("XC60","SUV"),("XC90","SUV")],
    "Lincoln": [("MKZ","Sedan"),("Nautilus","SUV"),("Aviator","SUV"),("Navigator","SUV")],
    "Cadillac": [("ATS","Sedan"),("CTS","Sedan"),("XT5","SUV"),("Escalade","SUV")],
    "Land Rover": [("Range Rover","SUV"),("Discovery","SUV"),("Range Rover Sport","SUV"),("Range Rover Evoque","SUV")],
    "Jaguar": [("XE","Sedan"),("XF","Sedan"),("F-Pace","SUV"),("E-Pace","SUV")],
    "Porsche": [("911","Coupe"),("Panamera","Sedan"),("Macan","SUV"),("Cayenne","SUV"),("Taycan","Sedan")],
    "Alfa Romeo": [("Giulia","Sedan"),("Stelvio","SUV")],
    "Genesis": [("G70","Sedan"),("G80","Sedan"),("GV70","SUV"),("GV80","SUV")],
    "Mini": [("Cooper","Hatchback"),("Countryman","SUV")],
    "Fiat": [("500","Hatchback"),("500X","SUV")],
    "Tesla": [("Model 3","Sedan"),("Model Y","SUV"),("Model S","Sedan"),("Model X","SUV")],
    "Rivian": [("R1T","Truck"),("R1S","SUV")],
    "Lucid": [("Air","Sedan")],
    "Polestar": [("2","Hatchback")],
    "Aston Martin": [("Vantage","Coupe"),("DB11","Coupe")],
    "Maserati": [("Ghibli","Sedan"),("Levante","SUV")],
    "Bentley": [("Continental GT","Coupe"),("Bentayga","SUV")],
    "Rolls-Royce": [("Ghost","Sedan"),("Cullinan","SUV")]
}

luxury_brands = {
    "BMW","Mercedes-Benz","Audi","Lexus","Acura","Infiniti","Volvo","Lincoln",
    "Cadillac","Land Rover","Jaguar","Porsche","Alfa Romeo","Genesis",
    "Aston Martin","Maserati","Bentley","Rolls-Royce",
    "Tesla","Rivian","Lucid","Polestar"
}

# ============================================================
# BASELINE BRAND WEIGHTS
# ============================================================
baseline_brand_weights = {
    "Toyota":1.5,"Honda":1.4,"Ford":1.6,"Chevrolet":1.6,"Nissan":1.2,
    "Hyundai":1.1,"Kia":1.1,"Volkswagen":0.9,"Subaru":0.9,"Mazda":0.8,
    "Jeep":0.9,"Dodge":0.7,"Ram":0.9,"GMC":0.7,"Buick":0.5,
    "Chrysler":0.4,"Mitsubishi":0.4,
    "BMW":0.8,"Mercedes-Benz":0.8,"Audi":0.7,"Lexus":0.7,
    "Acura":0.6,"Infiniti":0.5,"Volvo":0.4,
    "Lincoln":0.4,"Cadillac":0.5,
    "Land Rover":0.3,"Jaguar":0.2,"Porsche":0.2,
    "Alfa Romeo":0.1,"Genesis":0.2,"Mini":0.2,"Fiat":0.1,
    "Tesla":0.5,"Rivian":0.05,"Lucid":0.05,"Polestar":0.05,
    "Aston Martin":0.02,"Maserati":0.05,"Bentley":0.01,"Rolls-Royce":0.005
}

def market_brand_weights(market):
    w = baseline_brand_weights.copy()

    if market == "Los Angeles":
        for b in luxury_brands:
            if b in w: w[b] *= 1.6
        for b in ["Ram","GMC","Jeep","Dodge"]:
            if b in w: w[b] *= 0.7

    elif market == "Dallas":
        for b in ["Ford","Chevrolet","Ram","GMC","Jeep","Dodge"]:
            if b in w: w[b] *= 1.6
        for b in ["Tesla","Rivian","Lucid","Polestar"]:
            if b in w: w[b] *= 0.5

    elif market == "Columbus":
        for b in ["Toyota","Honda","Ford","Chevrolet","Nissan","Hyundai","Kia","Subaru","Mazda"]:
            if b in w: w[b] *= 1.2

    total = sum(w.values())
    brands = list(w.keys())
    probs = [w[b]/total for b in brands]
    return brands, probs

# ============================================================
# PRICE & MILEAGE LOGIC
# ============================================================
base_price_by_year = {
    2018:20000, 2019:22000, 2020:24000, 2021:27000,
    2022:30000, 2023:32000, 2024:34000, 2025:36000
}

def avg_mileage(year):
    age = 2025 - year
    return max(15000, min(12000*age + 10000, 160000))

def price_factor(brand, body, market, fuel):
    f = 1.0
    if brand in luxury_brands: f *= 1.7
    if body in {"Truck","SUV"}: f *= 1.1
    if market == "Los Angeles" and fuel == "Electric": f *= 1.2
    if market == "Dallas" and body == "Truck": f *= 1.2
    return f

# ============================================================
# GENERATE CLEAN DATA FIRST
# ============================================================
rows = []

print(f"Generating {N_ROWS:,} clean rows...")

for i in range(N_ROWS):
    market = np.random.choice(markets, p=market_prob)
    city = market
    state = cities[market]["state"]
    zip_code = random.choice(cities[market]["zips"])

    brands, probs = market_brand_weights(market)
    brand = np.random.choice(brands, p=probs)
    model, body = random.choice(brand_models[brand])

    year = np.random.randint(2018, 2026)
    avg_mi = avg_mileage(year)

    if market == "Dallas" and body == "Truck":
        avg_mi *= 1.15
    if market == "Los Angeles" and body in {"Sedan","Hatchback"}:
        avg_mi *= 0.9

    mileage = int(np.random.normal(avg_mi, 12000))
    mileage = max(5000, min(mileage, 220000))

    fuel = "Electric" if brand in {"Tesla","Rivian","Lucid","Polestar"} else \
           np.random.choice(["Gasoline","Hybrid","Electric","Diesel"], p=[0.7,0.15,0.1,0.05])

    transmission = np.random.choice(["Automatic","Manual","CVT"], p=[0.8,0.1,0.1])

    base_price = base_price_by_year[year]
    price = int(max(5000, min(base_price * price_factor(brand, body, market, fuel) +
                              np.random.normal(0,3500), 180000)))

    condition = np.random.choice(["Excellent","Good","Fair","Poor"], p=[0.4,0.4,0.15,0.05])
    seller_type = np.random.choice(["Dealer","Private Party"], p=[0.6,0.4])

    listing_date = datetime.now() - timedelta(days=np.random.randint(0,900))

    rows.append([
        price, year, mileage, brand, model, body, fuel, transmission,
        city, state, zip_code, listing_date.date().isoformat(),
        condition, seller_type, market
    ])

    if (i+1) % 50_000 == 0:
        print(f"  {i+1:,} rows generated...")

df = pd.DataFrame(rows, columns=[
    "price","year","mileage","make","model","body_type","fuel","transmission",
    "city","state","zip","listing_date","condition","seller_type","market"
])

print("Clean dataset shape:", df.shape)

# ============================================================
# INJECT MODERATE NOISE (missing + unrealistic)
# ============================================================
print("Injecting missing values and unrealistic values...")

def inject_missing(df, col, pct):
    mask = np.random.rand(len(df)) < pct
    df.loc[mask, col] = np.nan

missing_config = {
    "mileage":0.05, "condition":0.05, "seller_type":0.05,
    "fuel":0.03, "transmission":0.03, "body_type":0.03,
    "price":0.01, "year":0.01, "make":0.01, "model":0.01
}

for col, pct in missing_config.items():
    inject_missing(df, col, pct)

# Inject unrealistic values
n_unrealistic = int(len(df) * 0.008)

# Negative mileage
idx = np.random.choice(df.index, n_unrealistic//4, replace=False)
df.loc[idx, "mileage"] = -100

# Mileage too high
idx = np.random.choice(df.index, n_unrealistic//4, replace=False)
df.loc[idx, "mileage"] = 999999

# Price anomalies
idx = np.random.choice(df.index, n_unrealistic//4, replace=False)
df.loc[idx, "price"] = 0

idx = np.random.choice(df.index, n_unrealistic//4, replace=False)
df.loc[idx, "price"] = 999999

# Year anomalies
idx = np.random.choice(df.index, n_unrealistic//4, replace=False)
df.loc[idx, "year"] = 2050

idx = np.random.choice(df.index, n_unrealistic//4, replace=False)
df.loc[idx, "year"] = 1980

# Invalid body types
idx = np.random.choice(df.index, n_unrealistic//4, replace=False)
df.loc[idx, "body_type"] = "Unknown"

print("Noise injection complete.")

# ============================================================
# SAVE
# ============================================================
df.to_csv("used_car_data.csv", index=False)
print("Saved dataset as used_car_data.csv")
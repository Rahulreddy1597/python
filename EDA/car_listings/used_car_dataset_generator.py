import numpy as np
import pandas as pd

# -------------------- Catalog --------------------
def get_make_model_catalog():
    return {
        # Mass-market
        "Toyota": {
            "tier": "mass",
            "models": [
                {"name": "Camry", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "Corolla", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "RAV4", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
                {"name": "Prius", "body_style": "Hatchback", "drivetrain": "FWD", "fuel_type": "Hybrid"},
            ],
        },
        "Honda": {
            "tier": "mass",
            "models": [
                {"name": "Civic", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "Accord", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "CR-V", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
            ],
        },
        "Ford": {
            "tier": "mass",
            "models": [
                {"name": "F-150", "body_style": "Truck", "drivetrain": "4WD", "fuel_type": "Gas"},
                {"name": "Escape", "body_style": "SUV", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "Explorer", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
            ],
        },
        "Chevrolet": {
            "tier": "mass",
            "models": [
                {"name": "Silverado", "body_style": "Truck", "drivetrain": "4WD", "fuel_type": "Gas"},
                {"name": "Equinox", "body_style": "SUV", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "Malibu", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
            ],
        },
        "Nissan": {
            "tier": "mass",
            "models": [
                {"name": "Altima", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "Sentra", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "Rogue", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
            ],
        },
        "Hyundai": {
            "tier": "mass",
            "models": [
                {"name": "Elantra", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "Sonata", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "Tucson", "body_style": "SUV", "drivetrain": "FWD", "fuel_type": "Gas"},
            ],
        },
        "Kia": {
            "tier": "mass",
            "models": [
                {"name": "Forte", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "Optima", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "Sportage", "body_style": "SUV", "drivetrain": "FWD", "fuel_type": "Gas"},
            ],
        },

        # Luxury - German
        "BMW": {
            "tier": "luxury",
            "models": [
                {"name": "3 Series", "body_style": "Sedan", "drivetrain": "RWD", "fuel_type": "Gas"},
                {"name": "5 Series", "body_style": "Sedan", "drivetrain": "RWD", "fuel_type": "Gas"},
                {"name": "X3", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
                {"name": "X5", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Diesel"},
            ],
        },
        "Mercedes-Benz": {
            "tier": "luxury",
            "models": [
                {"name": "C-Class", "body_style": "Sedan", "drivetrain": "RWD", "fuel_type": "Gas"},
                {"name": "E-Class", "body_style": "Sedan", "drivetrain": "RWD", "fuel_type": "Gas"},
                {"name": "GLC", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
                {"name": "GLE", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Diesel"},
            ],
        },
        "Audi": {
            "tier": "luxury",
            "models": [
                {"name": "A4", "body_style": "Sedan", "drivetrain": "AWD", "fuel_type": "Gas"},
                {"name": "A6", "body_style": "Sedan", "drivetrain": "AWD", "fuel_type": "Gas"},
                {"name": "Q5", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
                {"name": "Q7", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Diesel"},
            ],
        },
        "Porsche": {
            "tier": "luxury",
            "models": [
                {"name": "Macan", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
                {"name": "Cayenne", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
                {"name": "Panamera", "body_style": "Sedan", "drivetrain": "AWD", "fuel_type": "Gas"},
            ],
        },

        # Luxury - Japanese
        "Lexus": {
            "tier": "luxury",
            "models": [
                {"name": "ES", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "IS", "body_style": "Sedan", "drivetrain": "RWD", "fuel_type": "Gas"},
                {"name": "NX", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Hybrid"},
                {"name": "RX", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
            ],
        },
        "Acura": {
            "tier": "luxury",
            "models": [
                {"name": "TLX", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "RDX", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
                {"name": "MDX", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
            ],
        },
        "Infiniti": {
            "tier": "luxury",
            "models": [
                {"name": "Q50", "body_style": "Sedan", "drivetrain": "RWD", "fuel_type": "Gas"},
                {"name": "QX60", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
            ],
        },

        # Luxury - American
        "Cadillac": {
            "tier": "luxury",
            "models": [
                {"name": "XT5", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
                {"name": "Escalade", "body_style": "SUV", "drivetrain": "4WD", "fuel_type": "Gas"},
            ],
        },
        "Lincoln": {
            "tier": "luxury",
            "models": [
                {"name": "MKZ", "body_style": "Sedan", "drivetrain": "FWD", "fuel_type": "Gas"},
                {"name": "Navigator", "body_style": "SUV", "drivetrain": "4WD", "fuel_type": "Gas"},
            ],
        },

        # Luxury - European Premium
        "Land Rover": {
            "tier": "luxury",
            "models": [
                {"name": "Discovery", "body_style": "SUV", "drivetrain": "4WD", "fuel_type": "Diesel"},
                {"name": "Range Rover Evoque", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
                {"name": "Range Rover Sport", "body_style": "SUV", "drivetrain": "4WD", "fuel_type": "Gas"},
            ],
        },
        "Volvo": {
            "tier": "luxury",
            "models": [
                {"name": "XC60", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Hybrid"},
                {"name": "XC90", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "Gas"},
            ],
        },

        # Electric luxury
        "Tesla": {
            "tier": "luxury",
            "models": [
                {"name": "Model 3", "body_style": "Sedan", "drivetrain": "RWD", "fuel_type": "EV"},
                {"name": "Model Y", "body_style": "SUV", "drivetrain": "AWD", "fuel_type": "EV"},
                {"name": "Model S", "body_style": "Sedan", "drivetrain": "AWD", "fuel_type": "EV"},
            ],
        },
    }

# -------------------- Base Prices --------------------
BASE_PRICE_BY_MODEL = {
    "Camry": 27000, "Corolla": 23000, "RAV4": 30000, "Prius": 28000,
    "Civic": 24000, "Accord": 28000, "CR-V": 31000,
    "F-150": 40000, "Escape": 28000, "Explorer": 36000,
    "Silverado": 39000, "Equinox": 27000, "Malibu": 25000,
    "Altima": 25000, "Sentra": 21000, "Rogue": 28000,
    "Elantra": 21000, "Sonata": 24000, "Tucson": 27000,
    "Forte": 20500, "Optima": 24500, "Sportage": 27000,

    "3 Series": 45000, "5 Series": 60000, "X3": 50000, "X5": 65000,
    "C-Class": 44000, "E-Class": 62000, "GLC": 52000, "GLE": 70000,
    "A4": 43000, "A6": 60000, "Q5": 50000, "Q7": 65000,
    "Macan": 60000, "Cayenne": 80000, "Panamera": 90000,
    "ES": 42000, "IS": 41000, "NX": 46000, "RX": 52000,
    "TLX": 40000, "RDX": 45000, "MDX": 52000,
    "Q50": 42000, "QX60": 50000,
    "XT5": 52000, "Escalade": 90000,
    "MKZ": 40000, "Navigator": 85000,
    "Discovery": 65000, "Range Rover Evoque": 55000, "Range Rover Sport": 85000,
    "XC60": 48000, "XC90": 60000,
    "Model 3": 50000, "Model Y": 55000, "Model S": 90000,
}

# -------------------- Market Factors --------------------
MARKET_PRICE_FACTOR = {
    "Los Angeles": 1.10,
    "Dallas–Fort Worth": 1.00,
    "San Juan": 0.90,
}

# -------------------- Helper Functions --------------------
def _sample_buyer_age_and_income(rng, market):
    age = rng.integers(22, 75)
    if market == "San Juan":
        base_income = rng.normal(38000, 12000)
    elif market == "Dallas–Fort Worth":
        base_income = rng.normal(62000, 20000)
    else:
        base_income = rng.normal(78000, 26000)
    income = max(18000, base_income + (age - 40) * 600)
    return int(age), float(income)

def _age_group(age):
    if age < 25: return "18-24"
    if age < 35: return "25-34"
    if age < 45: return "35-44"
    if age < 55: return "45-54"
    if age < 65: return "55-64"
    return "65+"

def _income_bracket(income):
    if income < 30000: return "Low"
    if income < 60000: return "Lower-Mid"
    if income < 90000: return "Upper-Mid"
    if income < 140000: return "High"
    return "Very High"

def _sample_purchase_type(rng, market, tier):
    if market == "San Juan":
        probs = {"Finance": 0.65, "Lease": 0.10, "Cash": 0.25}
    elif market == "Dallas–Fort Worth":
        probs = {"Finance": 0.55, "Lease": 0.20, "Cash": 0.25}
    else:
        probs = {"Finance": 0.40, "Lease": 0.45, "Cash": 0.15}
    if tier == "luxury":
        probs["Lease"] += 0.10
        probs["Cash"] -= 0.05
        probs["Finance"] -= 0.05
    keys = list(probs.keys())
    vals = np.array(list(probs.values()))
    vals = np.clip(vals, 0, None)
    vals = vals / vals.sum()
    return rng.choice(keys, p=vals)

def _sample_loan_terms(rng, purchase_type, tier):
    if purchase_type == "Cash":
        return 0, 0.0
    if purchase_type == "Lease":
        term = rng.choice([24, 36, 39, 42])
        rate = rng.uniform(0.001, 0.004)
        return term, rate
    if tier == "luxury":
        term = rng.choice([48, 60, 72])
    else:
        term = rng.choice([36, 48, 60, 72])
    rate = rng.uniform(0.02, 0.08)
    return term, rate

def _monthly_payment(principal, annual_rate, term_months):
    if term_months <= 0 or principal <= 0:
        return 0.0
    r = annual_rate / 12.0
    if r <= 0:
        return principal / term_months
    return float(principal * (r * (1 + r) ** term_months) / ((1 + r) ** term_months - 1))

# -------------------- Dataset Generator --------------------
def generate_dataset(output_path="car_sales_data.csv", n_rows=1_000_000, seed=42):
    rng = np.random.default_rng(seed)
    markets = ["Los Angeles", "Dallas–Fort Worth", "San Juan"]
    market_probs = [0.45, 0.35, 0.20]
    catalog = get_make_model_catalog()

    # Flatten catalog
    flat_models = []
    for make, info in catalog.items():
        for m in info["models"]:
            flat_models.append({
                "make": make,
                "model": m["name"],
                "tier": info["tier"],
                "body_style": m["body_style"],
                "drivetrain": m["drivetrain"],
                "fuel_type": m["fuel_type"],
                "base_price": BASE_PRICE_BY_MODEL[m["name"]],
            })
    flat_models_df = pd.DataFrame(flat_models)

    # Luxury share per market
    luxury_share_target = {
        "Los Angeles": (0.25, 0.35),
        "Dallas–Fort Worth": (0.10, 0.15),
        "San Juan": (0.05, 0.08),
    }

    # Base dataframe
    df = pd.DataFrame({
        "sale_id": np.arange(1, n_rows + 1),
        "market": rng.choice(markets, size=n_rows, p=market_probs),
    })

    # Sale dates
    start_date = pd.Timestamp("2015-01-01")
    end_date = pd.Timestamp("2025-12-31")
    df["sale_date"] = start_date + pd.to_timedelta(
        rng.integers(0, (end_date - start_date).days + 1, size=n_rows), unit="D"
    )

    # Model years
    years = np.arange(2015, 2026)
    year_probs = np.array([0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.10, 0.12, 0.15, 0.15, 0.15])
    year_probs /= year_probs.sum()
    df["model_year"] = rng.choice(years, size=n_rows, p=year_probs)

    # Vehicle tier
    df["vehicle_tier"] = [
        "luxury" if rng.random() < rng.uniform(*luxury_share_target[m]) else "mass"
        for m in df["market"]
    ]

    # Sample make/model
    make = np.empty(n_rows, dtype=object)
    model = np.empty(n_rows, dtype=object)
    body_style = np.empty(n_rows, dtype=object)
    drivetrain = np.empty(n_rows, dtype=object)
    fuel_type = np.empty(n_rows, dtype=object)
    base_price = np.empty(n_rows)
    for i, (tier, market) in enumerate(zip(df["vehicle_tier"], df["market"])):
        pool = flat_models_df[flat_models_df["tier"] == tier]
        if market == "San Juan":
            # Reduce chance of SUVs/Trucks
            large_suv = pool["body_style"].isin(["SUV", "Truck"])
            weights = np.where(large_suv, 0.1, 1.0)
            weights /= weights.sum()
            idx = rng.choice(pool.index, p=weights)
        elif market == "Dallas–Fort Worth":
            # More trucks
            trucks = pool["body_style"] == "Truck"
            weights = np.where(trucks, 3.0, 1.0)
            weights /= weights.sum()
            idx = rng.choice(pool.index, p=weights)
        else:
            idx = rng.choice(pool.index)
        row = pool.loc[idx]
        make[i] = row["make"]
        model[i] = row["model"]
        body_style[i] = row["body_style"]
        drivetrain[i] = row["drivetrain"]
        fuel_type[i] = row["fuel_type"]
        base_price[i] = row["base_price"]

    df["make"] = make
    df["model"] = model
    df["body_style"] = body_style
    df["drivetrain"] = drivetrain
    df["fuel_type"] = fuel_type
    df["base_price"] = base_price

    # Trim
    trims = ["Base", "Sport", "Luxury", "Limited"]
    trim_probs = [0.5, 0.25, 0.15, 0.10]
    df["trim"] = rng.choice(trims, size=n_rows, p=trim_probs)
    trim_factor = {"Base": 1.0, "Sport": 1.05, "Luxury": 1.1, "Limited": 1.15}
    df["trim_factor"] = df["trim"].map(trim_factor)

    # Vehicle age, price
    df["vehicle_age"] = (df["sale_date"].dt.year - df["model_year"]).clip(lower=0)
    market_factor = df["market"].map(MARKET_PRICE_FACTOR)
    age_discount = 1.0 - (df["vehicle_age"] * 0.04).clip(0, 0.6)
    noise = rng.normal(1.0, 0.08, size=n_rows)
    df["price"] = (df["base_price"] * df["trim_factor"] * market_factor * age_discount * noise).clip(5000, 200000)

    # Mileage
    mileage_base = rng.normal(12000, 4000, size=n_rows)
    df["mileage"] = (mileage_base * df["vehicle_age"]).clip(0, 250000).astype(int)

    # Condition grade
    cond = []
    for age, miles, tier in zip(df["vehicle_age"], df["mileage"], df["vehicle_tier"]):
        score = 5.0 - age*0.25 - (miles/20000)*0.5
        if tier=="luxury": score +=0.3
        if score>=4.5: cond.append("Excellent")
        elif score>=3.5: cond.append("Very Good")
        elif score>=2.5: cond.append("Good")
        elif score>=1.5: cond.append("Fair")
        else: cond.append("Poor")
    df["condition_grade"] = cond

    # Buyer demographics
    buyer_age = np.empty(n_rows, dtype=int)
    buyer_income = np.empty(n_rows)
    buyer_age_group = np.empty(n_rows, dtype=object)
    buyer_income_bracket = np.empty(n_rows, dtype=object)
    for i, market in enumerate(df["market"]):
        age, income = _sample_buyer_age_and_income(rng, market)
        buyer_age[i] = age
        buyer_income[i] = income
        buyer_age_group[i] = _age_group(age)
        buyer_income_bracket[i] = _income_bracket(income)
    df["buyer_age"] = buyer_age
    df["buyer_annual_income"] = buyer_income
    df["buyer_age_group"] = buyer_age_group
    df["buyer_income_bracket"] = buyer_income_bracket

    # Financing logic
    purchase_type = np.empty(n_rows, dtype=object)
    loan_term_months = np.zeros(n_rows, dtype=int)
    interest_rate = np.zeros(n_rows)
    down_payment = np.zeros(n_rows)
    monthly_payment = np.zeros(n_rows)
    payment_to_income_ratio = np.zeros(n_rows)
    for i, (market, tier, price, income) in enumerate(zip(df["market"], df["vehicle_tier"], df["price"], df["buyer_annual_income"])):
        ptype = _sample_purchase_type(rng, market, tier)
        purchase_type[i] = ptype

        if ptype=="Cash":
            loan_term_months[i]=0
            interest_rate[i]=0.0
            down = price*rng.uniform(0.6,1.0)
            down_payment[i]=down
            monthly_payment[i]=0.0
            payment_to_income_ratio[i]=(price-down)/max(income,1)
            continue

        if tier=="luxury":
            down = price*rng.uniform(0.15,0.30)
        else:
            down = price*rng.uniform(0.05,0.20)
        down_payment[i]=down

        term, rate = _sample_loan_terms(rng, ptype, tier)
        loan_term_months[i]=term
        interest_rate[i]=rate

        principal = price-down
        monthly_payment[i] = _monthly_payment(principal, rate, term)
        annual_payment = monthly_payment[i]*12
        payment_to_income_ratio[i] = annual_payment/max(income,1)

    df["purchase_type"]=purchase_type
    df["loan_term_months"]=loan_term_months
    df["interest_rate"]=interest_rate
    df["down_payment"]=down_payment
    df["monthly_payment"]=monthly_payment
    df["payment_to_income_ratio"]=payment_to_income_ratio

    # Inject nulls/unrealistic values
    mask_null_income = rng.random(n_rows) < 0.03
    df.loc[mask_null_income, ["buyer_annual_income","buyer_income_bracket"]]=np.nan
    mask_null_pti = rng.random(n_rows)<0.02
    df.loc[mask_null_pti,"payment_to_income_ratio"]=np.nan
    mask_unrealistic_price = rng.random(n_rows)<0.005
    df.loc[mask_unrealistic_price,"price"]*= rng.uniform(1.5,2.5, size=mask_unrealistic_price.sum())

    # Drop helper columns
    df=df.drop(columns=["base_price","trim_factor"])
    df.to_csv(output_path,index=False)
    print(f"Dataset with {n_rows} rows saved to {output_path}.")

# -------------------- Run --------------------
if __name__=="__main__":
    generate_dataset()

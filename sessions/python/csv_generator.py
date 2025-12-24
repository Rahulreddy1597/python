import pandas as pd
import numpy as np

# Seed for reproducibility
np.random.seed(101)

# Number of rows
n = 100

# Generate sample Titanic-like data
titanic_sample = pd.DataFrame({
    "PassengerId": np.arange(1, n+1),
    "Survived": np.random.choice([0,1], size=n),
    "Pclass": np.random.choice([1,2,3], size=n),
    "Name": ["Passenger_" + str(i) for i in range(1,n+1)],
    "Sex": np.random.choice(["male","female"], size=n),
    "Age": np.round(np.random.uniform(1, 80, size=n),1),
    "SibSp": np.random.randint(0, 3, size=n),
    "Parch": np.random.randint(0, 3, size=n),
    "Ticket": ["TCKT" + str(i) for i in range(1000, 1000+n)],
    "Fare": np.round(np.random.uniform(10, 500, size=n),2),
    "Cabin": np.random.choice([np.nan, "C123", "E45", "B78", "D56"], size=n),
    "Embarked": np.random.choice(["C", "Q", "S"], size=n)
})

# Save CSV locally
csv_path = "titanic_sample_100.csv"
titanic_sample.to_csv(csv_path, index=False)

print(f"Sample Titanic CSV file generated: {csv_path}")

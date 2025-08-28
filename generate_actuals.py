import pandas as pd
from faker import Faker
import random, os

fake = Faker()
customers = [f"CUST{i:03d}" for i in range(1, 21)]

# Accounting actuals
actuals = []
for i in range(100000):
    actuals.append({
        "TransactionID": i+1,
        "Date": fake.date_between(start_date="-6M", end_date="today"),
        "AccountCode": random.choice([6000,7000]),
        "Amount": round(random.uniform(100, 5000), 2) * random.choice([1, -1]),
        "Currency": "EUR",
        "CustomerID": random.choice(customers)
    })

pd.DataFrame(actuals).to_csv("./accounting_actuals.csv", index=False)
import pandas as pd
from faker import Faker
import random, os

fake = Faker()
customers = [f"CUST{i:03d}" for i in range(1, 21)]

# CRM pipeline
stages = ["Lead","Qualified","Proposal","Negotiation","Closed Won","Closed Lost"]
pipeline = []
for i in range(2000):
    pipeline.append({
        "OpportunityID": f"OPP{i+1:03d}",
        "CustomerID": random.choice(customers),
        "OpportunityName": fake.bs().title(),
        "Stage": random.choice(stages),
        "ExpectedCloseDate": fake.date_between(start_date="today", end_date="+3M"),
        "ExpectedRevenue": round(random.uniform(500, 20000), 2),
        "Owner": fake.first_name(),
        "Probability": random.choice([10,30,50,70,90])
    })

pd.DataFrame(pipeline).to_csv("./crm_data.csv", index=False)

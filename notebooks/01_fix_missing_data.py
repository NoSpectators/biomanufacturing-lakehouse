import os
import pandas as pd
import random
from faker import Faker

fake = Faker()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(os.path.join(RAW_DIR, "maintenance_logs"), exist_ok=True)
os.makedirs(os.path.join(RAW_DIR, "supply_chain"), exist_ok=True)

reactors = [f"R-{i}" for i in range(101, 106)]

# ---------------------------
# Maintenance Logs
# ---------------------------
maintenance = []

for i in range(300):
    maintenance.append({
        "maintenance_id": f"M-{1000+i}",
        "equipment_id": random.choice(reactors),
        "type": random.choice(["Calibration", "Repair", "Inspection"]),
        "downtime_minutes": random.randint(10, 500),
        "technician": fake.name(),
        "timestamp": fake.date_time_between("-60d", "now")
    })

pd.DataFrame(maintenance).to_csv(
    os.path.join(RAW_DIR, "maintenance_logs", "maintenance_logs.csv"),
    index=False
)

print("✔ maintenance_logs created")

# ---------------------------
# Supply Chain
# ---------------------------
shipments = []

for i in range(500):
    expected = random.randint(2, 10)
    actual = expected + random.randint(-1, 4)

    shipments.append({
        "shipment_id": f"S-{2000+i}",
        "supplier": fake.company(),
        "material": random.choice(["Glucose", "Enzymes", "Media"]),
        "expected_days": expected,
        "actual_days": actual,
        "delay_days": actual - expected
    })

pd.DataFrame(shipments).to_csv(
    os.path.join(RAW_DIR, "supply_chain", "supply_chain_shipments.csv"),
    index=False
)

print("✔ supply_chain created")

print("\nDone fixing missing raw datasets")
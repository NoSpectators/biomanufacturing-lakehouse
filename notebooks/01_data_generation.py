import os
import random
from datetime import timedelta
import pandas as pd
from faker import Faker

fake = Faker()

# ---------------------------------------------------
# Project root (IMPORTANT FIX)
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

# ---------------------------------------------------
# Ensure directories exist
# ---------------------------------------------------
folders = [
    "production_batches",
    "sensor_readings",
    "qa_lab_results",
    "maintenance_logs",
    "supply_chain"
]

for f in folders:
    os.makedirs(os.path.join(RAW_DIR, f), exist_ok=True)

# ---------------------------------------------------
# Config
# ---------------------------------------------------
NUM_BATCHES = 200
NUM_SENSORS = 5000

products = ["BioAmino-X", "FermaGrow", "CelluMax"]
reactors = [f"R-{i}" for i in range(101, 106)]

# ---------------------------------------------------
# Production Batches
# ---------------------------------------------------
batches = []

for i in range(NUM_BATCHES):
    start = fake.date_time_between("-60d", "-1d")
    end = start + timedelta(hours=random.randint(8, 72))

    batches.append({
        "batch_id": f"BATCH-{1000+i}",
        "product": random.choice(products),
        "reactor": random.choice(reactors),
        "start_time": start,
        "end_time": end,
        "yield_kg": round(random.uniform(500, 4000), 2),
        "status": random.choice(["Completed", "Failed"])
    })

pd.DataFrame(batches).to_csv(
    os.path.join(RAW_DIR, "production_batches", "production_batches.csv"),
    index=False
)

print("✔ production_batches created")

# ---------------------------------------------------
# Sensor Data
# ---------------------------------------------------
sensors = []

for _ in range(NUM_SENSORS):
    sensors.append({
        "timestamp": fake.date_time_between("-60d", "now"),
        "reactor": random.choice(reactors),
        "temp": round(random.uniform(28, 42), 2),
        "pressure": round(random.uniform(10, 40), 2),
        "ph": round(random.uniform(5.5, 7.5), 2)
    })

pd.DataFrame(sensors).to_csv(
    os.path.join(RAW_DIR, "sensor_readings", "sensor_readings.csv"),
    index=False
)

print("✔ sensor_readings created")

# ---------------------------------------------------
# QA Results
# ---------------------------------------------------
qa = []

for i in range(NUM_BATCHES):
    qa.append({
        "batch_id": f"BATCH-{1000+i}",
        "purity": round(random.uniform(90, 99.9), 2),
        "contaminated": random.choice([0, 0, 0, 1])
    })

pd.DataFrame(qa).to_csv(
    os.path.join(RAW_DIR, "qa_lab_results", "qa_lab_results.csv"),
    index=False
)

print("✔ QA results created")

print("\nDONE: All raw data generated successfully")
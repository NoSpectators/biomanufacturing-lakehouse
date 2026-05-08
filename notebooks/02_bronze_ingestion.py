from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp

# ---------------------------------------------------
# 1. Create Spark Session (Lakehouse Style)
# ---------------------------------------------------

spark = SparkSession.builder \
    .appName("BioManufacturing-Bronze-Layer") \
    .getOrCreate()

print("Spark session created")

# ---------------------------------------------------
# 2. File Paths
# ---------------------------------------------------

BASE_PATH = "data/raw"

paths = {
    "production_batches": f"{BASE_PATH}/production_batches/production_batches.csv",
    "sensor_readings": f"{BASE_PATH}/sensor_readings/sensor_readings.csv",
    "qa_lab_results": f"{BASE_PATH}/qa_lab_results/qa_lab_results.csv",
    "maintenance_logs": f"{BASE_PATH}/maintenance_logs/maintenance_logs.csv",
    "supply_chain": f"{BASE_PATH}/supply_chain/supply_chain_shipments.csv",
}

bronze_output = "data/bronze"

# ---------------------------------------------------
# 3. Generic Bronze Loader
# ---------------------------------------------------

def load_to_bronze(name, path):

    df = spark.read.csv(path, header=True, inferSchema=True)

    # Standardize ingestion metadata (VERY IMPORTANT in real jobs)
    df = df.withColumn("ingestion_time", current_timestamp())

    # Write as Delta (or parquet fallback if Delta not configured)
    output_path = f"{bronze_output}/{name}"

    df.write.mode("overwrite").parquet(output_path)

    print(f"Bronze table written: {name} -> {output_path}")

    return df

# ---------------------------------------------------
# 4. Ingest All Datasets into Bronze Layer
# ---------------------------------------------------

production_df = load_to_bronze("production_batches", paths["production_batches"])

sensor_df = load_to_bronze("sensor_readings", paths["sensor_readings"])

qa_df = load_to_bronze("qa_lab_results", paths["qa_lab_results"])

maintenance_df = load_to_bronze("maintenance_logs", paths["maintenance_logs"])

supply_df = load_to_bronze("supply_chain", paths["supply_chain"])

# ---------------------------------------------------
# 5. Quick Validation Checks
# ---------------------------------------------------

print("\n--- Bronze Layer Summary ---")

print("Production:", production_df.count())
print("Sensors:", sensor_df.count())
print("QA:", qa_df.count())
print("Maintenance:", maintenance_df.count())
print("Supply Chain:", supply_df.count())

print("\nBronze ingestion complete.")
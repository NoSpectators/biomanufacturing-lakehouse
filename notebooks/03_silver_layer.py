from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, when

# ---------------------------------------------------
# Spark session (no Delta yet — keep stable)
# ---------------------------------------------------
spark = SparkSession.builder \
    .appName("BioManufacturing-Silver-Layer") \
    .getOrCreate()

print("Spark started")

# ---------------------------------------------------
# Paths
# ---------------------------------------------------
RAW = "data/raw"
SILVER = "data/silver"

# ---------------------------------------------------
# Load Bronze (raw CSVs)
# ---------------------------------------------------
batches = spark.read.csv(f"{RAW}/production_batches/production_batches.csv", header=True, inferSchema=True)
sensors = spark.read.csv(f"{RAW}/sensor_readings/sensor_readings.csv", header=True, inferSchema=True)
qa = spark.read.csv(f"{RAW}/qa_lab_results/qa_lab_results.csv", header=True, inferSchema=True)
maintenance = spark.read.csv(f"{RAW}/maintenance_logs/maintenance_logs.csv", header=True, inferSchema=True)
supply = spark.read.csv(f"{RAW}/supply_chain/supply_chain_shipments.csv", header=True, inferSchema=True)

# ---------------------------------------------------
# 1. Clean Batches
# ---------------------------------------------------
silver_batches = batches \
    .dropna(subset=["batch_id"]) \
    .dropDuplicates(["batch_id"]) \
    .withColumn("yield_kg", col("yield_kg").cast("double"))

# ---------------------------------------------------
# 2. Clean Sensors (remove impossible values)
# ---------------------------------------------------
silver_sensors = sensors \
    .filter((col("temp") > 20) & (col("temp") < 60)) \
    .filter((col("ph") > 4) & (col("ph") < 9)) \
    .dropDuplicates()

# ---------------------------------------------------
# 3. Clean QA
# ---------------------------------------------------
silver_qa = qa \
    .dropDuplicates(["batch_id"]) \
    .withColumn("contaminated", col("contaminated").cast("int"))

# ---------------------------------------------------
# 4. Maintenance (basic cleanup)
# ---------------------------------------------------
silver_maintenance = maintenance.dropDuplicates()

# ---------------------------------------------------
# 5. Supply chain cleanup
# ---------------------------------------------------
silver_supply = supply.dropDuplicates()

# ---------------------------------------------------
# 6. Join: Batch + QA (core business dataset)
# ---------------------------------------------------
batch_quality = silver_batches.join(
    silver_qa,
    on="batch_id",
    how="left"
)

# ---------------------------------------------------
# 7. Compute batch performance KPIs
# ---------------------------------------------------
batch_performance = batch_quality \
    .groupBy("product", "reactor") \
    .agg(
        avg("yield_kg").alias("avg_yield"),
        count("batch_id").alias("total_batches"),
        avg("contaminated").alias("contamination_rate")
    )

# ---------------------------------------------------
# Write Silver outputs
# ---------------------------------------------------
silver_batches.write.mode("overwrite").parquet(f"{SILVER}/batches")
silver_sensors.write.mode("overwrite").parquet(f"{SILVER}/sensors")
silver_qa.write.mode("overwrite").parquet(f"{SILVER}/qa")
silver_maintenance.write.mode("overwrite").parquet(f"{SILVER}/maintenance")
silver_supply.write.mode("overwrite").parquet(f"{SILVER}/supply_chain")

batch_performance.write.mode("overwrite").parquet(f"{SILVER}/batch_performance")

print("\nSilver layer complete")

print("Batch performance rows:", batch_performance.count())
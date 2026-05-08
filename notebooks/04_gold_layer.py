from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, desc, when

spark = SparkSession.builder \
    .appName("BioManufacturing-Gold-Layer") \
    .getOrCreate()

print("Spark started")

# ---------------------------------------------------
# Load Silver datasets
# ---------------------------------------------------
SILVER = "data/silver"
GOLD = "data/gold"

batches = spark.read.parquet(f"{SILVER}/batches")
qa = spark.read.parquet(f"{SILVER}/qa")
performance = spark.read.parquet(f"{SILVER}/batch_performance")

# ---------------------------------------------------
# 1. Reactor Performance Score
# ---------------------------------------------------
reactor_perf = batches.groupBy("reactor").agg(
    avg("yield_kg").alias("avg_yield"),
    count("batch_id").alias("total_batches")
).orderBy(desc("avg_yield"))

# ---------------------------------------------------
# 2. Product Quality Risk Score
# ---------------------------------------------------
quality_risk = batches.join(qa, "batch_id", "left") \
    .groupBy("product") \
    .agg(
        avg("contaminated").alias("contamination_rate"),
        avg("yield_kg").alias("avg_yield")
    ) \
    .withColumn(
        "risk_score",
        col("contamination_rate") * 0.7 + (100 - col("avg_yield")) * 0.3
    )

# ---------------------------------------------------
# 3. Production Efficiency Index
# ---------------------------------------------------
efficiency = batches.groupBy("product").agg(
    avg("yield_kg").alias("avg_yield"),
    count("batch_id").alias("batch_count")
)

# ---------------------------------------------------
# Write Gold Tables
# ---------------------------------------------------
reactor_perf.write.mode("overwrite").parquet(f"{GOLD}/reactor_performance")
quality_risk.write.mode("overwrite").parquet(f"{GOLD}/quality_risk")
efficiency.write.mode("overwrite").parquet(f"{GOLD}/efficiency")

print("\nGold layer complete")

print("Reactors:", reactor_perf.count())
print("Products:", efficiency.count())
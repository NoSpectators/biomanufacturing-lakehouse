import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt

# ---------------------------------------------------
# Spark Session
# ---------------------------------------------------
spark = SparkSession.builder \
    .appName("BioManufacturing-Dashboard") \
    .getOrCreate()

# ---------------------------------------------------
# Load Gold Data
# ---------------------------------------------------
GOLD = "data/gold"

reactor_perf = spark.read.parquet(
    f"{GOLD}/reactor_performance"
).toPandas()

quality_risk = spark.read.parquet(
    f"{GOLD}/quality_risk"
).toPandas()

efficiency = spark.read.parquet(
    f"{GOLD}/efficiency"
).toPandas()

# ---------------------------------------------------
# Streamlit UI
# ---------------------------------------------------
st.title("BioManufacturing Lakehouse Analytics")

st.markdown("""
Enterprise analytics dashboard built with:
- PySpark
- Lakehouse architecture
- Gold KPI tables
- Streamlit
""")

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------
st.header("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Reactors",
    len(reactor_perf)
)

col2.metric(
    "Products",
    len(efficiency)
)

col3.metric(
    "Avg Yield",
    round(efficiency["avg_yield"].mean(), 2)
)

# ---------------------------------------------------
# Reactor Performance
# ---------------------------------------------------
st.header("Reactor Performance")

st.dataframe(reactor_perf)

fig, ax = plt.subplots()

ax.bar(
    reactor_perf["reactor"],
    reactor_perf["avg_yield"]
)

ax.set_xlabel("Reactor")
ax.set_ylabel("Average Yield")

st.pyplot(fig)

# ---------------------------------------------------
# Quality Risk
# ---------------------------------------------------
st.header("Quality Risk Scores")

st.dataframe(quality_risk)

fig2, ax2 = plt.subplots()

ax2.bar(
    quality_risk["product"],
    quality_risk["risk_score"]
)

ax2.set_xlabel("Product")
ax2.set_ylabel("Risk Score")

st.pyplot(fig2)

# ---------------------------------------------------
# Efficiency Table
# ---------------------------------------------------
st.header("Production Efficiency")

st.dataframe(efficiency)

st.success("Dashboard loaded successfully")
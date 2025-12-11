import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL

# ----------------------------------------
# IMPORT DETECT ANOMALIES & SUMMARIZER
# ----------------------------------------
from detect_anomalies import detect_anomalies
from generate_summary import summarize_anomalies

# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------
st.set_page_config(page_title="FinOps Spike & Drop Detector", layout="wide")
st.title("FinOps Cost Spike / Drop Detection Dashboard")

# ----------------------------------------
# ETL
# ----------------------------------------
DATA_CSV = "mock_billing_90d.csv"
df = pd.read_csv(DATA_CSV, parse_dates=["date"])

# Clean numeric columns
df["cost"] = pd.to_numeric(df["cost"], errors="coerce").fillna(0)
df["usage"] = pd.to_numeric(df["usage"], errors="coerce").fillna(0)
df["service"] = df["service"].fillna("Unknown")

# Service selection
svc = st.selectbox("Select service", sorted(df["service"].unique()))
df_s = df[df["service"] == svc].sort_values("date").reset_index(drop=True)

# ----------------------------------------
# DETECT ANOMALIES
# ----------------------------------------
df_s = detect_anomalies(df_s)

# ----------------------------------------
# PLOT SECTION WITH DRIFT VISUALIZATION
# ----------------------------------------
st.subheader(f"Cost Time Series & Anomalies for {svc}")

fig, ax = plt.subplots(figsize=(12, 5))

# Base cost plot
ax.plot(df_s["date"], df_s["cost"], label="Cost")

# Separate anomaly types
anom_spike = df_s[df_s["anomaly_type"] == "spike"]
anom_drop = df_s[df_s["anomaly_type"] == "drop"]
anom_drift = df_s[df_s["anomaly_type"] == "drift"]

# Spike scatter
if not anom_spike.empty:
    ax.scatter(anom_spike["date"], anom_spike["cost"], label="Spike", zorder=4)

# Drop scatter
if not anom_drop.empty:
    ax.scatter(anom_drop["date"], anom_drop["cost"], label="Drop", zorder=4)

# Drift scatter
if not anom_drift.empty:
    ax.scatter(anom_drift["date"], anom_drift["cost"], label="Drift", marker="D", s=70, zorder=5)
    # Drift rolling trend
    drift_trend = df_s["cost"].rolling(7).mean()
    ax.plot(df_s["date"], drift_trend, linestyle=":", label="Drift Trend")

# STL trend line
if len(df_s) >= 7:
    stl = STL(df_s["cost"], period=7, robust=True)
    res = stl.fit()
    ax.plot(df_s["date"], res.trend, linestyle="--", label="Trend")

ax.set_xlabel("Date")
ax.set_ylabel("Cost (USD)")
ax.legend()
st.pyplot(fig)

# ----------------------------------------
# AI SUMMARY WITH EXPLANATIONS
# ----------------------------------------
st.subheader("AI Summary of Detected Anomalies")

@st.cache_data(show_spinner=False)
def cached_summary(df_service):
    return summarize_anomalies(df_service)

if st.button("Generate Summary"):
    with st.spinner("Generating summary..."):
        try:
            summary_text = cached_summary(df_s)
            st.info(summary_text)
        except Exception as e:
            st.error(f"Summary generation failed: {e}")

# ----------------------------------------
# TABLE OF DETECTED ANOMALIES
# ----------------------------------------
st.subheader(f"Detected Anomalies for {svc}")
anom_points = df_s[df_s["anomaly_any"]]

if not anom_points.empty:
    st.table(
        anom_points[["date", "service", "cost", "usage", "anomaly_type"]].rename(
            columns={
                "date": "Date",
                "service": "Service",
                "cost": "Cost",
                "usage": "Usage",
                "anomaly_type": "Type"
            }
        )
    )
else:
    st.write("No anomalies detected for this service.")

from statsmodels.tsa.seasonal import STL
import pandas as pd

def detect_anomalies(df):
    """
    Detects anomalies in cost data:
      - spike: sudden large increase
      - drop: sudden large decrease
      - drift: gradual sustained increase
    Returns a dataframe with anomaly flags, types, and explanations.
    """

    df = df.copy()
    df = df.sort_values("date").reset_index(drop=True)

    # Initialize anomaly columns
    df["anomaly_any"] = False
    df["anomaly_type"] = None
    df["explanation"] = None

    # Need at least 7 data points for STL
    if len(df) < 7:
        return df

    # -----------------------
    # Spike / Drop detection
    # -----------------------
    stl = STL(df["cost"], period=7, robust=True)
    res = stl.fit()
    residual = res.resid

    q1 = residual.quantile(0.25)
    q3 = residual.quantile(0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    for i in range(len(df)):
        if residual.iloc[i] > upper:
            df.at[i, "anomaly_any"] = True
            df.at[i, "anomaly_type"] = "spike"
            df.at[i, "explanation"] = (
                "Cost significantly exceeded historical trend. Likely driven by a usage spike, auto-scaling burst, or short-lived workload expansion."
            )
        elif residual.iloc[i] < lower:
            df.at[i, "anomaly_any"] = True
            df.at[i, "anomaly_type"] = "drop"
            df.at[i, "explanation"] = (
                "Cost dropped well below expected trend. Possibly due to workload decommissioning, resource optimization, or reduced demand."
            )

    # -----------------------
    # Drift detection (gradual increase)
    # -----------------------
    rolling_mean = df["cost"].rolling(7).mean()
    slope = rolling_mean.diff()
    drift_threshold = slope.mean() + 2 * slope.std()
    drift_mask = slope > drift_threshold

    for i in df.index[drift_mask]:
        # If already marked as spike/drop, append drift
        if df.at[i, "anomaly_any"]:
            df.at[i, "anomaly_type"] += " + drift"
            df.at[i, "explanation"] += " | Gradual sustained increase in cost indicating potential configuration drift, usage growth, or scaling changes."
        else:
            df.at[i, "anomaly_any"] = True
            df.at[i, "anomaly_type"] = "drift"
            df.at[i, "explanation"] = (
                "Gradual sustained increase in cost indicating potential configuration drift, usage growth, or scaling changes."
            )

    return df

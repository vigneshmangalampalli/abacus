from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model
MODEL_NAME = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def summarize_anomalies(df):
    """
    Summarizes anomalies by date, including types and context.
    Combines multiple anomalies on the same day.
    """
    anomalies = df[df["anomaly_any"]]

    if anomalies.empty:
        return "No anomalies detected for this service."

    # ---- GROUP ANOMALIES BY DATE ----
    grouped = (
        anomalies.groupby("date")
        .agg({
            "cost": "first",
            "anomaly_type": lambda x: " + ".join(sorted(set(x))),
            "explanation": lambda x: " | ".join(sorted(set(x)))
        })
        .reset_index()
    )

    records = []
    for _, row in grouped.iterrows():
        date_str = row["date"].strftime('%Y-%m-%d')
        records.append(
            f"Date: {date_str}, "
            f"Cost: {row['cost']}, "
            f"Types: {row['anomaly_type']}, "
            f"Context: {row['explanation']}"
        )

    # ---- JOIN ALL RECORDS INTO PROMPT ----
    final_summary = "\n".join(records)
    return final_summary

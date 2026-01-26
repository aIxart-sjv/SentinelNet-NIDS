import joblib
import pandas as pd
import numpy as np
import time


# Load trained components
model = joblib.load("../models/xgboost.pkl")
scaler = joblib.load("../models/scaler.pkl")

def detect(df):
    X = df.copy()
    X_scaled = scaler.transform(X)
    predictions = model.predict(X_scaled)
    return predictions

if __name__ == "__main__":
    print("🚀 SentinelNet IDS Started")

    # Example: load a sample file
    sample_file = "../data/raw/DDoS-Friday-no-metadata.parquet"
    df = pd.read_parquet(sample_file)

    # Take small batch for demo
    df = df.sample(50)

    # Remove label if exists
    if "Label" in df.columns:
        df = df.drop(columns=["Label"])

    preds = detect(df)

    for i, p in enumerate(preds):
        status = "🚨 ATTACK" if p == 1 else "✅ BENIGN"
        print(f"[LIVE] Flow {i+1}: {status}")
        time.sleep(1)   # simulate live delay
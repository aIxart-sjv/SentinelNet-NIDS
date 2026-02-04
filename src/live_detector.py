import csv
from datetime import datetime
from scapy.all import sniff, IP, TCP
import joblib
import numpy as np
import os

# ===============================
# Load trained model and scaler
# ===============================
model = joblib.load("../models/xgboost.pkl")
scaler = joblib.load("../models/scaler.pkl")

print("🚀 SentinelNet LIVE IDS Started...")

# ===============================
# Log file setup
# ===============================
LOG_FILE = "../results/live_logs.csv"
os.makedirs("../results", exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "prediction"])

# ===============================
# Feature extraction
# ===============================
def extract_features(packet):
    if IP not in packet:
        return None

    ip = packet[IP]
    proto = ip.proto
    length = len(packet)

    features = [
        proto,
        length,
        packet.time % 1000,
        int(TCP in packet),
    ]

    return np.array(features).reshape(1, -1)

# ===============================
# Packet processing
# ===============================
def process_packet(packet):
    features = extract_features(packet)
    if features is None:
        return

    padded = np.zeros((1, 77))
    padded[0, :features.shape[1]] = features

    scaled = scaler.transform(padded)
    prediction = model.predict(scaled)[0]

    label = "ATTACK" if prediction == 1 else "BENIGN"

    # Console output
    if label == "ATTACK":
        print("🚨 ATTACK DETECTED!")
    else:
        print("✅ Normal traffic")

    # Log to CSV for dashboard
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), label])

# ===============================
# Start sniffing
# ===============================
print("🟢 Listening on Ethernet interface...")

sniff(prn=process_packet, store=False)  # Change interface as needed

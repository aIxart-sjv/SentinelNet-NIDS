import csv
from datetime import datetime
from scapy.all import sniff, IP, TCP
import joblib
import numpy as np
import os
import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ===============================
# Load model
# ===============================
model = joblib.load("../models/xgboost.pkl")
scaler = joblib.load("../models/scaler.pkl")

print("🚀 SentinelNet LIVE IDS Started...")

# ===============================
# FastAPI setup
# ===============================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# In-memory storage (IMPORTANT)
# ===============================
logs = []

# ===============================
# CSV backup (optional now)
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

    features = [
        ip.proto,
        len(packet),
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

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prediction": label
    }

    # Console output
    if label == "ATTACK":
        print("🚨 ATTACK DETECTED!")
    else:
        print("✅ Normal traffic")

    # Log to CSV for dashboard
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([log_entry["timestamp"], label])

# ===============================
# Sniffer thread
# ===============================
def start_sniffing():
    print("🟢 Listening for packets...")
    sniff(prn=process_packet, store=False)

# ===============================
# API endpoint
# ===============================
print("🟢 Listening on Ethernet interface...")

sniff(prn=process_packet, store=False)  # Change interface as needed

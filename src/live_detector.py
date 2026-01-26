from scapy.all import sniff, IP, TCP
import joblib
import numpy as np
import time

# Load trained model and scaler
model = joblib.load("../models/xgboost.pkl")
scaler = joblib.load("../models/scaler.pkl")

print("🚀 SentinelNet LIVE IDS Started...")

flow_stats = {}

def extract_features(packet):
    if IP not in packet:
        return None

    ip = packet[IP]
    proto = ip.proto
    length = len(packet)

    # Simple features (demo version)
    features = [
        proto,
        length,
        packet.time % 1000,
        int(TCP in packet),
    ]

    return np.array(features).reshape(1, -1)

def process_packet(packet):
    features = extract_features(packet)
    if features is None:
        return

    # Pad to match model input size (demo trick)
    padded = np.zeros((1, 77))
    padded[0, :features.shape[1]] = features

    scaled = scaler.transform(padded)
    prediction = model.predict(scaled)[0]

    if prediction == 1:
        print("🚨 ATTACK DETECTED!")
    else:
        print("✅ Normal traffic")

sniff(prn=process_packet, store=False)

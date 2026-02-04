import streamlit as st
import pandas as pd
import os
import time

# ===============================
# Config
# ===============================
LOG_FILE = "../results/live_logs.csv"
REFRESH_SEC = 2

st.set_page_config(
    page_title="SentinelNet IDS",
    layout="wide"
)

# ===============================
# Title & Status
# ===============================
st.title("🛡️ SentinelNet – Live Intrusion Detection Dashboard")
st.markdown("Real‑time AI‑powered Network Intrusion Detection System")

st.success("🟢 System Status: LIVE")

# ===============================
# Load Data
# ===============================
if not os.path.exists(LOG_FILE):
    st.warning("Waiting for live traffic data...")
    time.sleep(REFRESH_SEC)
    st.experimental_rerun()

df = pd.read_csv(LOG_FILE)

if df.empty:
    st.warning("No packets captured yet...")
    time.sleep(REFRESH_SEC)
    st.experimental_rerun()

# ===============================
# Pre‑processing
# ===============================
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["attack_flag"] = df["prediction"].apply(
    lambda x: 1 if x == "ATTACK" else 0
)

total_flows = len(df)
attacks = df["attack_flag"].sum()
benign = total_flows - attacks

# ===============================
# Metrics Row
# ===============================
col1, col2, col3 = st.columns(3)

col1.metric("📊 Total Flows", total_flows)
col2.metric("🚨 Attacks Detected", attacks)
col3.metric("✅ Benign Traffic", benign)

# ===============================
# Timeline
# ===============================
st.subheader("📈 Live Detection Timeline")

timeline = (
    df.set_index("timestamp")
      .resample("5S")["attack_flag"]
      .sum()
)

st.line_chart(timeline)

# ===============================
# Recent Events
# ===============================
st.subheader("📋 Recent Network Events")
st.dataframe(
    df.tail(15),
    use_container_width=True
)

# ===============================
# Auto Refresh
# ===============================
st.caption(f"Auto‑refreshing every {REFRESH_SEC} seconds")
time.sleep(REFRESH_SEC)
st.rerun()

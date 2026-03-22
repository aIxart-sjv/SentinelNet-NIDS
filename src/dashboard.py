import streamlit as st
import pandas as pd
import os

# ===============================
# Config
# ===============================
LOG_FILE = "../results/live_logs.csv"

st.set_page_config(page_title="SentinelNet IDS", layout="wide")

# ===============================
# Title
# ===============================
st.title("🛡️ SentinelNet – Live Intrusion Detection Dashboard")
st.markdown("Real‑time AI‑powered Network Intrusion Detection System")
st.success("🟢 System Status: LIVE")

# ===============================
# Load Data
# ===============================
if not os.path.exists(LOG_FILE):
    st.warning("Waiting for live traffic data...")
    st.stop()

df = pd.read_csv(LOG_FILE)

if df.empty:
    st.warning("No packets captured yet...")
    st.stop()

# ===============================
# Processing
# ===============================
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["attack_flag"] = df["prediction"].apply(
    lambda x: 1 if x == "ATTACK" else 0
)

total = len(df)
attacks = df["attack_flag"].sum()
benign = total - attacks

# ===============================
# Metrics
# ===============================
col1, col2, col3 = st.columns(3)

col1.metric("📊 Total Flows", total)
col2.metric("🚨 Attacks Detected", attacks)
col3.metric("✅ Benign Traffic", benign)

# ===============================
# Timeline
# ===============================
st.subheader("📈 Live Detection Timeline")

timeline = (
    df.set_index("timestamp")
      .resample("5s")["attack_flag"]
      .sum()
)

st.line_chart(timeline)

# ===============================
# Table
# ===============================
st.subheader("📋 Recent Network Events")
st.dataframe(df.tail(15), use_container_width=True)

# ===============================
# Auto Refresh (SAFE)
# ===============================
st.caption("🔄 Auto-refreshing every 2 seconds")

from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=2000, key="refresh")
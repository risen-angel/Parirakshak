import streamlit as st
import pandas as pd
from utils import calculate_scores

st.title("Bridge Status Page")
st.subheader("Bridge Vibration & Camera Monitoring")


bridges = calculate_scores(bridges)
# Load data
try:
    bridges = pd.read_csv("data/bridges.csv")
except:
    st.error("bridges.csv file not found or empty.")
    st.stop()

# ---- SCORING LOGIC MOVED HERE ----

# Calculate damage
bridges["damage"] = (
    (20.83 * bridges["vibration"]) +
    (0.25 * bridges["stress"]) +
    (50 * bridges["crack"])
)

# Calculate health score
bridges["score"] = 100 - bridges["damage"]
bridges["score"] = bridges["score"].clip(0, 100)

# Assign status
def get_status(score):
    if score >= 90:
        return "green"
    elif score >= 70:
        return "yellow"
    else:
        return "red"

bridges["status"] = bridges["score"].apply(get_status)

# -----------------------------------

# Bridge selection
bridge = st.selectbox("Select Bridge", bridges["name"])

selected = bridges[bridges["name"] == bridge].iloc[0]

st.write(f"### Details for {bridge}")

st.metric("Health Score", round(selected["score"], 2))

if selected["status"] == "green":
    st.success("🟢 Safe")
elif selected["status"] == "yellow":
    st.warning("🟡 Warning")
else:
    st.error("🔴 Critical")

st.write("Vibration:", selected["vibration"])
st.write("Stress:", selected["stress"])
st.write("Crack:", selected["crack"])





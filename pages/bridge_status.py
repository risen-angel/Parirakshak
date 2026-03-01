import streamlit as st
import pandas as pd

st.title("Bridge Status Page")
st.subheader("Bridge Vibration & Camera Monitoring")

try:
    bridges = pd.read_csv("data/bridges.csv")
except:
    st.error("bridges.csv file not found or empty.")
    st.stop()

bridge = st.selectbox("Select Bridge", bridges["name"])
st.write(f"You selected: {bridge}")




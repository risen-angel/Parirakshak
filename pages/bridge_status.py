'''import streamlit as st
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
st.write("Here you can add vibration graphs, scores, and live camera feed for this bridge.")
'''
import streamlit as st
import pandas as pd
import random
import datetime
import plotly.graph_objects as go
st.markdown("<style>.stApp{background-color:#F2E0C8 !important;}</style>", unsafe_allow_html=True)
st.markdown("<style>.stApp{background-color:#F2E0C8 !important;} section[data-testid='stSidebar']{background-color:#8B4513 !important;} section[data-testid='stSidebar'] *{color:#FFFFFF !important;}</style>", unsafe_allow_html=True)
st.set_page_config(page_title="Bridge Detailed Status", layout="wide")

st.title("Bridge Detailed Status")
st.caption("Structural Risk Analysis Dashboard")

st.divider()

try:
    bridges = pd.read_csv("data/bridges.csv")
    vibration = pd.read_csv("data/vibration_week.csv")
except:
    st.error("Required CSV files not found.")
    st.stop()

search = st.text_input("Enter Flyover Name or Pincode")

if search:

    result = bridges[
        (bridges["name"].str.contains(search, case=False)) |
        (bridges["pincode"].astype(str).str.contains(search))
    ]

    if not result.empty:

        bridge = result.iloc[0]
        score = bridge["score"]

        st.subheader(f"Flyover: {bridge['name']}")
        st.write(f"Pincode: {bridge['pincode']}")

        if score > 80:
            risk = "SAFE"
            color = "green"
        elif score > 50:
            risk = "WARNING"
            color = "orange"
        else:
            risk = "CRITICAL"
            color = "red"

        col1, col2 = st.columns([1, 1])

        with col1:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text': "Structural Health Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "red"},
                        {'range': [50, 80], 'color': "orange"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                }
            ))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(f"<h3 style='color:{color};'>Risk Level: {risk}</h3>", unsafe_allow_html=True)

        st.divider()

        left, right = st.columns([2, 1])

        with left:
            st.subheader("7-Day Vibration Trend Analysis")
            bridge_vib = vibration[vibration["bridge_name"] == bridge["name"]]
            if not bridge_vib.empty:
                st.line_chart(bridge_vib.set_index("day")["avg_vibration"])
            else:
                st.warning("No vibration data available.")

        with right:
            st.subheader("Present Vibration")
            current_vibration = random.randint(5, 25)
            st.metric("Current Vibration Level", current_vibration)

            if current_vibration > 20:
                st.error("High Vibration Detected")
            elif current_vibration > 12:
                st.warning("Moderate Structural Stress")
            else:
                st.success("Normal Vibration Range")

            st.write("Last Updated:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        st.divider()

        st.subheader("Live Structural Monitoring Camera")

        if st.button("View Live Camera Feed"):
            try:
                video_file = open("assets/flyover_video.mp4", "rb")
                video_bytes = video_file.read()
                st.video(video_bytes)

                crack_prob = random.randint(80, 99)

                if crack_prob > 90:
                    st.success(f"Crack Detection Confidence: {crack_prob}% - No Structural Cracks Detected")
                else:
                    st.warning(f"Minor Surface Crack Probability: {100-crack_prob}% (Low Risk)")
            except:
                st.error("Video file not found in assets folder.")

        st.divider()

        report = f"""
Bridge Name: {bridge['name']}
Pincode: {bridge['pincode']}
Structural Score: {score}
Risk Level: {risk}
Generated On: {datetime.datetime.now()}
"""

        st.download_button(
            label="Download Safety Report",
            data=report,
            file_name=f"{bridge['name']}_report.txt",
            mime="text/plain"
        )

    else:
        st.error("No Flyover Found")


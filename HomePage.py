import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Parirakshak", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #F2E0C8;
    color: #2D5A27;
}

section[data-testid="stSidebar"] {
    background-color: #8B4513;
}
section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;   /* ← ADD THIS */
}
h1, h2, h3, h4 {
    color: #FFFFFF;
}

/* Metric cards */
.card-container {
    display: flex;
    gap: 20px;
    margin-top: 20px;
}
.card {
    flex: 1;
    padding: 25px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
}
.safe { background-color: #27AE60; }
.warning { background-color: #F39C12; }
.critical { background-color: #E74C3C; }
.card .count { font-size: 40px; }
.card .label { font-size: 18px; }

hr { border: 1px solid #2C3E50; }

.blink {
    animation: blinker 1s linear infinite;
    color: #E74C3C;
    font-weight: bold;
    font-size: 20px;
}
@keyframes blinker { 50% { opacity: 0; } }

/* Force input labels and page link to white */
[data-baseweb="input"] label {
    color: white !important;
}
a[data-testid="stPageLink"] {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
if "logged_in" not in st.session_state:
    USERS = {
    "admin": "1234",
    "engineer": "eng123"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "users" not in st.session_state:
    st.session_state.users = USERS  # starts with default users

def login_page():
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        st.subheader("Sign Up")
        new_user = st.text_input("Choose Username", key="signup_user")
        new_pass = st.text_input("Choose Password", type="password", key="signup_pass")
        confirm  = st.text_input("Confirm Password", type="password", key="signup_confirm")
        if st.button("Sign Up"):
            if not new_user or not new_pass:
                st.warning("Please fill all fields.")
            elif new_user in st.session_state.users:
                st.error("Username already exists!")
            elif new_pass != confirm:
                st.error("Passwords don't match!")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Account created! Please login.")
if not st.session_state.logged_in:
    login_page()
    st.stop()

col1, col2 = st.columns([8, 2])
with col1:
    st.title("Parirakshak")
    st.caption("Real-Time Structural Health Monitoring Dashboard")
with col2:
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()


st.divider()

try:
    bridges = pd.read_csv("data/bridges.csv")
except:
    st.error("bridges.csv file not found or empty.")
    st.stop()

green_count = len(bridges[bridges["status"] == "green"])
yellow_count = len(bridges[bridges["status"] == "yellow"])
red_count = len(bridges[bridges["status"] == "red"])

st.markdown(f"""
<div class="card-container">
    <div class="card safe">
        <div class="count">{green_count}</div>
        <div class="label">🟢 Safe Bridges</div>
    </div>
    <div class="card warning">
        <div class="count">{yellow_count}</div>
        <div class="label">🟡 Warning Bridges</div>
    </div>
    <div class="card critical">
        <div class="count">{red_count}</div>
        <div class="label">🔴 Critical Bridges</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

if red_count > 0:
    st.markdown('<p class="blink">🔴 ALERT: Critical Flyover Requires Immediate Inspection</p>', unsafe_allow_html=True)

st.subheader("Bridge Status Map")
left, right = st.columns([4, 1])

with left:
    m = folium.Map(location=[10.8, 78.7], zoom_start=7)
    color_map = {"green": "green", "yellow": "orange", "red": "red"}

    for _, row in bridges.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=7,
            color=color_map[row["status"]],
            fill=True,
            fill_color=color_map[row["status"]],
            fill_opacity=0.9,
            popup=f"""
            <b>{row['name']}</b><br>
            Pincode: {row['pincode']}<br>
            Status: {row['status'].upper()}<br>
            Score: {row['score']}
            """
        ).add_to(m)

    st_folium(m, width=700, height=450)

with right:
    st.markdown("### Status Legend")
    st.markdown("🟢 Safe")
    st.markdown("🟡 Warning")
    st.markdown("🔴 Critical")

st.divider()

st.subheader("Search Flyover")
search = st.text_input("Enter Flyover Name or Pincode")

if search:
    result = bridges[
        (bridges["name"].str.contains(search, case=False)) |
        (bridges["pincode"].astype(str).str.contains(search))
    ]
    if not result.empty:
        st.success("Flyover Found")
        st.dataframe(result)
    else:
        st.error("No Flyover Found")

st.divider()
st.page_link("pages/bridge_status.py", label="Go to Bridge Status Page")



import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ---------------------- Page Config ----------------------
st.set_page_config(page_title="Parirakshak", layout="wide")

# ---------------------- CSS Styling ----------------------
st.markdown("""
<style>
.stApp {
    background-color: #F2E0C8 !important;
    color: #000000 !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #F2E0C8 !important;
}
section[data-testid="stSidebar"] {
    background-color: #8B4513 !important;
}
section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
h1, h2, h3, h4 {
    color: #000000 !important;
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

# ---------------------- Session State Login ----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123"}

def login_page():
    st.title("Parirakshak Login System")
    option = st.radio("Select Option", ["Login", "Sign Up"])
    if option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")
    elif option == "Sign Up":
        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")
        if st.button("Register"):
            if new_user in st.session_state.users:
                st.warning("User already exists")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Please login.")

if not st.session_state.logged_in:
    login_page()
    st.stop()

# ---------------------- Sidebar ----------------------
st.sidebar.title("Smart Flyover Dashboard")
st.sidebar.header("Navigation")
st.sidebar.write("Home")
st.sidebar.write("Bridge Status")  # Streamlit automatically links this page if it exists in pages/
st.sidebar.markdown("---")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------------- Header ----------------------
col1, col2 = st.columns([8, 2])
with col1:
    st.title("Parirakshak")
    st.caption("Real-Time Structural Health Monitoring Dashboard")
with col2:
    st.write("Admin Panel")

st.divider()

# ---------------------- Load Data ----------------------
try:
    bridges = pd.read_csv("data/bridges.csv")
except:
    st.error("bridges.csv file not found or empty.")
    st.stop()

green_count = len(bridges[bridges["status"] == "green"])
yellow_count = len(bridges[bridges["status"] == "yellow"])
red_count = len(bridges[bridges["status"] == "red"])

# ---------------------- Metric Cards ----------------------
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

# ---------------------- Alert ----------------------
if red_count > 0:
    st.markdown('<p class="blink">🔴 ALERT: Critical Flyover Requires Immediate Inspection</p>', unsafe_allow

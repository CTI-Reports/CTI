import streamlit as st
from core.data_loader import fetch_reports_from_github, load_local_reports

st.set_page_config(
    page_title="ML Threat Intelligence",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject CSS & JS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open("assets/scripts.js") as f:
    st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

st.markdown(
    "<h1 class='glow-text'>ML-Powered Threat Intelligence Platform</h1>",
    unsafe_allow_html=True,
)

st.write("Use the left sidebar to navigate between **Dashboard**, **ML Intelligence**, and **About**.")

# Optionally pre-fetch reports from GitHub
fetch_reports_from_github()
_ = load_local_reports()  # just to validate presence

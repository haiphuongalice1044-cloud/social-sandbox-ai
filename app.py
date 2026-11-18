
import streamlit as st
import pandas as pd
import html
from datetime import datetime

# =====================================================
# 1. CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Social Sandbox AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

NAVY = "#00246B"
ICE = "#CADCFC"
WHITE = "#FFFFFF"
BLACK = "#000000"

# =====================================================
# 2. DESIGN SYSTEM
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800;900&display=swap');

.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(202,220,252,.15), transparent 25%),
        radial-gradient(circle at 85% 75%, rgba(202,220,252,.12), transparent 25%),
        linear-gradient(135deg,#00143D,#00246B,#00143D);
    font-family:'Be Vietnam Pro',sans-serif;
}

/* MAIN CONTENT */
.main .block-container {
    max-width:1450px;
    padding:2rem 2.5rem 3rem;
}

/* OUTSIDE TEXT */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp p,
.stApp li,
.stApp label,
.stApp .stMarkdown,
.stApp .stCaption,
.stApp [data-testid="stMetricLabel"] {
    color:#FFFFFF;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#CADCFC,#FFFFFF);
}
section[data-testid="stSidebar"] * {
    color:#000000 !important;
}

/* HEADER */
.main-title {
    font-size:36px;
    font-weight:900;
    color:#FFFFFF;
    letter-spacing:-1px;
}
.main-subtitle {
    color:#CADCFC;
    font-size:13px;
    font-weight:600;
    letter-spacing:1px;
    margin-bottom:25px;
}

/* HERO */
.hero {
    background:linear-gradient(120deg,#FFFFFF,#CADCFC);
    padding:30px;
    border-radius:22px;
    margin-bottom:24px;
    box-shadow:0 10px 30px rgba(0,0,0,.2);
}
.hero * {
    color:#00246B !important;
}

/* LIGHT CARDS */
.light-card {
    background:linear-gradient(145deg,#FFFFFF,#EDF4FF);
    

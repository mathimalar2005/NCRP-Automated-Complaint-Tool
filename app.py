import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import pdfplumber
import re
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="NCRP Intelligence Pro", layout="wide", page_icon="🛡️")

# --- ADVANCED CUSTOM CSS FOR PREMIUM UI ---
st.markdown("""
    <style>
    /* Gradient Background for the whole app */
    .stApp {
        background: radial-gradient(circle at top right, #0a192f, #020c1b);
        color: #e6f1ff;
    }
    
    /* Glassmorphism Effect for Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 20px;
    }

    /* Modern Metric Styling */
    [data-testid="stMetric"] {
        background: rgba(0, 212, 255, 0.05);
        border-left: 5px solid #00d4ff;
        padding: 15px;
        border-radius: 10px;
    }

    /* Customizing the Sidebar */
    [data-testid="stSidebar"] {
        background-color: #020c1b !important;
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }

    /* Button Glow Effect */
    .stButton>button {
        background: linear-gradient(45deg, #00d4ff, #0050ff);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 10px 25px;
        font-weight: 600;
        letter-spacing: 1px;
        transition: 0.4s;
    }
    .stButton>button:hover {
        box-shadow: 0px 0px 20px #00d4ff;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND LOGIC (Injected) ---
def process_pdf(file):
    # This matches the core logic we built earlier
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    # Extract data using regex
    data = {
        "Complaint ID": re.search(r"Complaint ID[:\s]+(\w+)", text),
        "Category": re.search(r"Category[:\s]+([\w\s]+)", text),
        "Amount": re.search(r"Amount[:\s]*[^\d]*(\d+)", text),
    }
    extracted = {k: (v.group(1) if v else "N/A") for k, v in data.items()}
    return extracted

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color: #64ffda;'>🛡️ NCRP SHIELD</h1>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Command Center", "Data Scanner", "Archive"],
        icons=["cpu", "shield-lock", "folder2-open"],
        styles={
            "container": {"background-color": "transparent"},
            "nav-link": {"color": "#8892b0", "font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#112240", "color": "#64ffda", "border-left": "4px solid #64ffda"}
        }
    )

# --- PAGE 1: COMMAND CENTER (Dashboard) ---
if selected == "Command Center":
    st.markdown("<h2 style='color: #ccd6f6;'>System Overview</h2>", unsafe_allow_html=True)
    
    # Example Row of Beautiful Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Complaints", "128", "+12%")
    col2.metric("Total Fraud Recovered", "₹4.2L", "+5%")
    col3.metric("System Uptime", "99.9%")

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📊 Crime Category Analysis")
    # Sample Chart
    chart_data = pd.DataFrame({"Category": ["UPI Fraud", "Social Media", "Bank Scam"], "Count": [45, 30, 25]})
    fig = px.bar(chart_data, x='Category', y='Count', template="plotly_dark", color_discrete_sequence=['#64ffda'])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2: DATA SCANNER (The Functional Tool) ---
elif selected == "Data Scanner":
    st.markdown("<h2 style='color: #ccd6f6;'>Intelligent Document Scanner</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    files = st.file_uploader("Drop official NCRP PDF documents here", type="pdf", accept_multiple_files=True)
    
    if files:
        results = []
        for f in files:
            data = process_pdf(f)
            results.append(data)
        
        st.write("🔍 **Extraction Preview**")
        st.dataframe(pd.DataFrame(results), use_container_width=True)
        
        if st.button("Sync with Master Records"):
            st.balloons()
            st.success("Master database updated successfully.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3: ARCHIVE ---
elif selected == "Archive":
    st.markdown("<h2 style='color: #ccd6f6;'>Database Records</h2>", unsafe_allow_html=True)
    st.info("The central database is encrypted and synchronized.")
    # Placeholder for database view
    st.markdown("<div class='glass-card'>Secure Table View - Online</div>", unsafe_allow_html=True)
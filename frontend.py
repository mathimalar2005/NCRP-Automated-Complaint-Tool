import streamlit as st
import pandas as pd
import os
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from backend import extract_ncrp_details, update_database
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="NCRP | FORENSIC UNIT", layout="wide", page_icon="🕵️")

# --- HIGH-TECH MATTE DARK THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #B0B0B0; }
    [data-testid="stMetric"] { background: #1E1E1E !important; border: 1px solid #333333 !important; border-radius: 10px; padding: 15px; }
    .stButton>button { background: linear-gradient(135deg, #2C3E50, #000000); color: #00d4ff; border: 1px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- RISK CALCULATION LOGIC ---
def get_risk_level(amount):
    try:
        amt = float(amount)
        if amt > 100000: return "🔴 HIGH", "#FF4B4B"
        elif amt > 25000: return "🟡 MEDIUM", "#FFD700"
        else: return "🟢 LOW", "#00FF00"
    except:
        return "⚪ UNKNOWN", "#808080"

# --- LOGIN GATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    cols = st.columns([1, 1.5, 1])
    with cols[1]:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #707070;'>SECURE ACCESS TERMINAL</h2>", unsafe_allow_html=True)
        user_id = st.text_input("OFFICER IDENTIFICATION")
        access_key = st.text_input("SECURE ACCESS KEY", type="password")
        if st.button("EXECUTE LOGIN"):
            if user_id == "ADMIN" and access_key == "NCRP2026":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Authentication Failed.")
else:
    # --- AUTHENTICATED SIDEBAR ---
    with st.sidebar:
        st.markdown("<h3 style='color: #00d4ff;'>UNIT: CYBER-FORENSICS</h3>", unsafe_allow_html=True)
        selected = option_menu(
            menu_title=None,
            options=["Evidence Scanner", "Command Center", "Criminal Database"],
            icons=["fingerprint", "activity", "archive"], 
            menu_icon="shield-lock", default_index=0,
            styles={"container": {"background-color": "#121212"}, "nav-link-selected": {"background-color": "#333333", "color": "#00d4ff"}}
        )
        if st.button("TERMINATE SESSION"):
            st.session_state['logged_in'] = False
            st.rerun()

    # --- PAGE 1: EVIDENCE SCANNER ---
    if selected == "Evidence Scanner":
        st.header("🔍 Digital Evidence Extraction")
        uploaded_files = st.file_uploader("", type="pdf", accept_multiple_files=True)
        if uploaded_files:
            results = []
            for f in uploaded_files:
                data = extract_ncrp_details(f)
                label, color = get_risk_level(data.get('Amount', 0))
                data['Risk Level'] = label # Add Risk Level to the data
                results.append(data)
            
            st.dataframe(pd.DataFrame(results), use_container_width=True)
            if st.button("UPLOAD TO CENTRAL ARCHIVE"):
                update_database(results)
                st.toast("Evidence Recorded with Risk Assessment.", icon="💾")
                st.balloons()

    # --- PAGE 2: COMMAND CENTER ---# --- PAGE 2: COMMAND CENTER ---
    elif selected == "Command Center":
        st.markdown("<h2 style='color: #00d4ff;'>📊 STRATEGIC OPERATIONS COMMAND</h2>", unsafe_allow_html=True)
        
        if os.path.exists("NCRP_Master.xlsx"):
            df = pd.read_excel("NCRP_Master.xlsx")
            
            # 1. Metrics Row at the top
            m1, m2, m3 = st.columns(3)
            m1.metric("INVESTIGATIONS", len(df))
            m2.metric("ASSET LOSS", f"INR {pd.to_numeric(df['Amount'], errors='coerce').sum():,.2f}")
            m3.metric("STATUS", "SECURE", delta="AES-256")

            st.divider()

            # 2. THE ANALYTICS AREA (Where you use the code)
            col_chart, col_intel = st.columns([2, 1]) # Chart gets more space, Intel gets less

            with col_chart:
                st.subheader("📈 Threat Distribution")
                # Your chart code here...
                fig = px.bar(df, x='Category', template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            with col_intel:
                # --- PASTE THE INTEL SUMMARY CODE HERE ---
                st.subheader("🚩 Intel Summary")
                try:
                    mode_series = df['Category'].mode()
                    primary_threat = mode_series[0] if not mode_series.empty else "DETERMINING..."
                except:
                    primary_threat = "ANALYZING DATA"

                st.markdown(f"""
                <div style='background: #1E1E1E; padding: 20px; border-radius: 10px; border-left: 5px solid #00d4ff;'>
                    <p style='color: #808080; margin-bottom: 5px; font-size: 0.8rem;'>PRIMARY THREAT:</p>
                    <h4 style='color: #e6f1ff; margin-top: 0;'>{primary_threat}</h4>
                    <p style='color: #808080; margin-bottom: 5px; font-size: 0.8rem; margin-top: 15px;'>SYSTEM INTEGRITY:</p>
                    <h4 style='color: #00FF00; margin-top: 0;'>ACTIVE / 100%</h4>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.warning("No data found in Master Archive.")
  # --- PAGE 3: CRIMINAL DATABASE ---
    elif selected == "Criminal Database":
        st.header("🗄️ Master Record Repository")
        if os.path.exists("NCRP_Master.xlsx"):
            df_master = pd.read_excel("NCRP_Master.xlsx")
            
            # SAFE CHECK: Only apply colors if Risk Level exists
            if 'Risk Level' in df_master.columns:
                def color_risk(val):
                    if "HIGH" in str(val): return 'color: #FF4B4B; font-weight: bold'
                    elif "MEDIUM" in str(val): return 'color: #FFD700'
                    elif "LOW" in str(val): return 'color: #00FF00'
                    return ''
                st.dataframe(df_master.style.applymap(color_risk, subset=['Risk Level']), use_container_width=True)
            else:
                st.dataframe(df_master, use_container_width=True)
        else:
            st.error("Archived data not found.")
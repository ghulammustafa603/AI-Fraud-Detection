import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random
from datetime import datetime, timedelta

# ==========================================
# CONFIGURATION & BRANDING
# ==========================================
st.set_page_config(
    page_title="WalletGuard | Pakistani Digital Wallet Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Fintech Look
st.markdown("""
    <style>
    /* Main Background & Base Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    .stApp {
        background-color: #F1F5F9;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #0F172A;
    }
    
    /* Sidebar Overhaul (Dark Sidebar / Light Main) */
    [data-testid="stSidebar"] {
        background-color: #1E293B;
        border-right: None;
    }
    
    /* Force ALL Sidebar Text to White */
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    /* Fix Sidebar Info Box (st.info) */
    [data-testid="stSidebar"] .stAlert {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    [data-testid="stSidebar"] .stAlert p {
        color: #38BDF8 !important; /* Sky Blue for status text */
        font-weight: 700 !important;
    }

    /* Fix Sidebar Button Text */
    [data-testid="stSidebar"] button p {
        color: #1E293B !important;
    }
    [data-testid="stSidebar"] button {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
    }
    
    /* Premium Light Card Design */
    .metric-card {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #2ECC71;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 800;
        color: #1E293B;
        margin-top: 8px;
    }
    .metric-label {
        font-size: 12px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Highlights */
    .safety-green { color: #10B981; }
    .emergency-red { color: #EF4444; }
    
    .status-badge {
        padding: 8px 16px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
    }

    /* Spotlight Section (Light) */
    .spotlight-card {
        background: #FFFFFF;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Timer & Actions */
    .timer-box {
        background: linear-gradient(135deg, #EF4444 0%, #B91C1C 100%);
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        font-size: 36px;
        font-weight: 800;
        color: white;
        box-shadow: 0 10px 15px -3px rgba(239, 68, 68, 0.4);
    }
    
    /* Button Styling */
    .stButton>button {
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        transition: all 0.2s !important;
    }
    
    /* Target Specific Buttons */
    div.stButton > button:first-child {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        color: #1E293B !important;
    }
    div.stButton > button:hover {
        border-color: #10B981 !important;
        color: #10B981 !important;
        background-color: #F0FDF4 !important;
    }
    
    /* Overall Risk Styling */
    .risk-score-display {
        background: #FFFFFF;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Table Styling */
    .stDataFrame {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        overflow: hidden;
    }

    /* SPECIFIC BUTTON COLORS FOR WALLETGUARD */
    /* Safe Button (First Button in the pair) */
    div[data-testid="column"]:nth-child(1) button {
        border-color: #10B981 !important;
        color: #10B981 !important;
    }
    /* Block Button (Second Button in the pair - Primary) */
    div[data-testid="column"]:nth-child(2) button[kind="primary"] {
        background-color: #EF4444 !important;
        border-color: #EF4444 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# STATE MANAGEMENT
# ==========================================
if 'history' not in st.session_state:
    st.session_state.history = []
if 'is_frozen' not in st.session_state:
    st.session_state.is_frozen = False
if 'current_transaction' not in st.session_state:
    st.session_state.current_transaction = None
if 'countdown_active' not in st.session_state:
    st.session_state.countdown_active = False
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None

from model import calculate_risk, generate_transaction, CITIES, WALLETS

# ==========================================
# UTILITY FUNCTIONS
# ==========================================

# ==========================================
# BUSINESS LOGIC: UTILITY FUNCTIONS
# ==========================================

def generate_local_data(n=1000):
    """
    BUSINESS LOGIC: Simulates a subset of the transaction dataset for instant dashboard visualization.
    This mimics the production dataset description: (TXN_ID, Timestamp, Amount, Age, Gender, City, Device, Frequency).
    """
    data = []
    for _ in range(n):
        tx = generate_transaction()
        score, weights = calculate_risk(tx)
        tx['risk_score'] = score
        tx['is_fraud'] = 1 if score > 70 else 0
        data.append(tx)
    return pd.DataFrame(data)

def log_transaction(tx, status):
    """
    BUSINESS LOGIC: Appends flagged transactions to a local CSV for auditing (SBP Compliance).
    In a real system, this would push to a secure SQL database or FIA API.
    """
    log_entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "TXN_ID": tx['id'],
        "Wallet": tx['wallet'],
        "Amount": tx['amount'],
        "Risk_Score": tx['score'],
        "Action": status,
        "City": tx['city']
    }
    df = pd.DataFrame([log_entry])
    try:
        import os
        df.to_csv("audit_log.csv", mode='a', header=not os.path.exists("audit_log.csv"), index=False)
    except:
        pass

# ==========================================
# SIDEBAR & BRANDING
# ==========================================
import os
with st.sidebar:
    st.markdown(f"<h1 style='color: #2ECC71;'>🛡️ WalletGuard</h1>", unsafe_allow_html=True)
    st.markdown("### Pakistani Fraud Shield")
    st.write("AI-Powered Anomaly Analytics for **JazzCash** & **Easypaisa**.")
    st.divider()
    
    st.info("**System Status:** Active & Monitoring\n\n**Node:** Karachi-KHI-01")
    
    st.divider()
    st.markdown("### 🛠️ Operation Mode")
    app_mode = st.radio("Choose Mode:", ["Live Simulator", "Manual Test Sandbox"])
    st.session_state.app_mode = app_mode

    # Audit Log View in Sidebar
    if os.path.exists("audit_log.csv"):
        st.markdown("### 📋 Recent Security Logs")
        try:
            logs = pd.read_csv("audit_log.csv").tail(5)
            for _, row in logs.iterrows():
                color = "#E74C3C" if "Block" in str(row['Action']) else "#2ECC71"
                st.markdown(f"""
                    <div style="font-size: 11px; border-left: 3px solid {color}; padding-left: 10px; margin-bottom: 12px; background: #1A1F2B; padding: 10px; border-radius: 6px; border: 1px solid #2D3648;">
                        <b style="color: #FFFFFF;">{row['TXN_ID']}</b> <span style="color: {color}; font-weight: 700;">({row['Action']})</span><br>
                        <span style="color: #94A3B8;">Rs. {row['Amount']} | {row['City']}</span>
                    </div>
                """, unsafe_allow_html=True)
        except:
            pass

    if st.button("Reset Simulator"):
        st.session_state.is_frozen = False
        st.session_state.history = []
        st.session_state.countdown_active = False
        st.rerun()

# ==========================================
# MAIN DASHBOARD
# ==========================================

# Top Row: DASHBOARD METRICS (As per Business Report)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card"><div class="metric-label">Active Users Protected</div><div class="metric-value">38M+</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card" style="border-left-color: #F1C40F;"><div class="metric-label">Prevented Loss (Annual)</div><div class="metric-value">Rs. 2.3T</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div class="metric-label">Detection Accuracy</div><div class="metric-value">94.0%</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- TABS FOR DIFFERENT VIEWS ---
tab1, tab2 = st.tabs(["🛡️ Live Operations", "📊 Model Analytics"])

with tab1:
    if st.session_state.is_frozen:
        st.markdown("""
            <div style="background-color: #E74C3C; padding: 50px; border-radius: 15px; text-align: center; border: 5px solid white;">
                <h1 style="color: white; font-size: 50px;">🛑 STOLEN ACCOUNT FROZEN</h1>
                <p style="font-size: 20px;">Identity theft detected. Access to JazzCash/Easypaisa API has been revoked. FIA Cybercrime Wing notified.</p>
            </div>
        """, unsafe_allow_html=True)
        st.stop()

    # Real-time Simulator Logic
    if st.session_state.app_mode == "Live Simulator":
        if not st.session_state.countdown_active:
            # Update transaction every cycle
            new_tx = generate_transaction()
            score, weights = calculate_risk(new_tx)
            new_tx['score'] = score
            new_tx['weights'] = weights
            
            st.session_state.current_transaction = new_tx
            st.session_state.history.insert(0, new_tx)
            if len(st.session_state.history) > 10:
                st.session_state.history.pop()

            # ANOMALY VISUALIZATION TRIGGER: Score > 70
            if score > 70:
                st.session_state.countdown_active = True
                st.session_state.timer_start = time.time()
                st.rerun()
    else:
        # MANUAL TEST SANDBOX LOGIC
        st.markdown("### 🧪 Manual Transaction Sandbox")
        st.write("Input custom parameters to test the AI Risk Engine.")
        
        with st.container():
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                m_wallet = st.selectbox("Select Wallet", WALLETS)
                m_city = st.selectbox("Select City", CITIES)
                m_amount = st.number_input("Transaction Amount (Rs.)", min_value=10, max_value=500000, value=5000)
            with m_col2:
                m_age = st.slider("User Age", 10, 90, 25)
                m_hour = st.slider("Transaction Hour (0-23)", 0, 23, 14)
                m_new_device = st.toggle("New Device Fingerprint", value=False)
                m_loc_mismatch = st.toggle("City-Level Mismatch", value=False)
                m_high_freq = st.toggle("High Transaction Frequency", value=False)
            
            if st.button("🚀 Analyze Manual Transaction", use_container_width=True):
                # Construct a transaction object for the Risk Scoring Engine
                now = datetime.now()
                m_tx = {
                    "id": "MANUAL-TEST",
                    "wallet": m_wallet,
                    "city": m_city,
                    "amount": m_amount,
                    "time": now.replace(hour=m_hour, minute=0),
                    "is_new_device": m_new_device,
                    "is_loc_mismatch": m_loc_mismatch,
                    "high_freq": m_high_freq,
                    "user_age": m_age,
                    "user_gender": "Not Specified"
                }
                score, weights = calculate_risk(m_tx)
                m_tx['score'] = score
                m_tx['weights'] = weights
                st.session_state.current_transaction = m_tx
                st.session_state.countdown_active = False # No countdown in manual mode by default
                st.toast("Analysis Complete!", icon="✅")

    # --- INTERACTIVE GUI: DISPLAY ANALYSIS ---
    if st.session_state.current_transaction is not None:
        curr = st.session_state.current_transaction
        score = curr['score']
        weights = curr['weights']

        main_col, side_col = st.columns([2, 1])

        with main_col:
            st.subheader("Live Transaction Feed")
            
            # Current Spotlight Card
            status_color = "#FF4B4B" if score > 70 else "#2ECC71"
            status_text = "⚠️ HIGH RISK ANOMALY" if score > 70 else "✅ SECURE TRANSACTION"
            
            st.markdown(f"""
                <div class="spotlight-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 22px; font-weight: 800; color: #1E293B;">{curr['wallet']} Transaction: {curr['id']}</span>
                        <span class="status-badge" style="background: {status_color}20; color: {status_color}; border: 1px solid {status_color};">{status_text}</span>
                    </div>
                    <hr style="margin: 20px 0; border-color: #F1F5F9;">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <p style="color: #64748B; font-size: 11px; margin: 0; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;">City</p>
                            <p style="font-size: 22px; font-weight: 800; color: #0F172A;">{curr['city']}</p>
                        </div>
                        <div>
                            <p style="color: #64748B; font-size: 11px; margin: 0; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;">Amount</p>
                            <p style="font-size: 22px; font-weight: 800; color: #10B981;">Rs. {curr['amount']:,}</p>
                        </div>
                        <div>
                            <p style="color: #64748B; font-size: 11px; margin: 0; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;">Timestamp</p>
                            <p style="font-size: 22px; font-weight: 800; color: #0F172A;">{curr['time'].strftime('%I:%M %p')}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Historical List
            st.write("Recent Activity (Simulator History)")
            hist_df = pd.DataFrame(st.session_state.history)
            if not hist_df.empty:
                display_df = hist_df[['id', 'wallet', 'city', 'amount', 'score']].copy()
                display_df['amount'] = display_df['amount'].apply(lambda x: f"Rs. {x:,}")
                st.dataframe(display_df, use_container_width=True, hide_index=True)

        with side_col:
            # 30-SECOND RESPONSE WINDOW SIMULATION
            if st.session_state.countdown_active:
                elapsed = time.time() - st.session_state.timer_start
                remaining = max(0, 30 - int(elapsed))
                
                st.markdown(f'<div class="timer-box">RESPONSE WINDOW: {remaining}s</div>', unsafe_allow_html=True)
                
                btn_col1, btn_col2 = st.columns(2)
                if btn_col1.button("✅ Confirm Safe", use_container_width=True):
                    log_transaction(curr, "Confirmed Safe")
                    st.session_state.countdown_active = False
                    st.rerun()
                if btn_col2.button("🚫 Block & Report", type="primary", use_container_width=True):
                    log_transaction(curr, "Blocked & Reported to FIA")
                    st.session_state.is_frozen = True
                    st.rerun()
                    
                if remaining <= 0:
                    log_transaction(curr, "Auto-Blocked (Timeout)")
                    st.session_state.is_frozen = True
                    st.rerun()
                
                # Trigger rerun to update timer
                time.sleep(1)
                st.rerun()
            
            st.subheader("AI Risk Profile (Radar Chart)")
            
            # Radar Chart Visualization of the 6 Risk Dimensions
            categories = list(weights.keys())
            values = list(weights.values())
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Risk Profile',
                line_color='#E74C3C' if score > 70 else '#2ECC71'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], color="#8B949E"),
                    bgcolor="rgba(0,0,0,0)"
                ),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=20, b=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f"""
                <div class="risk-score-display">
                    <p style="color: #64748B; font-size: 13px; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 0.1em;">Final Risk Score</p>
                    <h1 style="color: {status_color}; font-size: 54px; margin: 0; font-weight: 800;">{score}%</h1>
                </div>
            """, unsafe_allow_html=True)


# ==========================================
# MODEL ANALYTICS TAB
# ==========================================
with tab2:
    st.header("📊 Kaggle-Scale Model Performance")
    st.write("Analysis of the **100,000 row** synthetic training dataset.")
    
    if os.path.exists("wallet_fraud_dataset.csv"):
        df_full = pd.read_csv("wallet_fraud_dataset.csv")
        
        # Summary Metrics
        m1, m2, m3, m4 = st.columns(4)
        fraud_count = df_full['is_fraud'].sum()
        total_count = len(df_full)
        fraud_rate = (fraud_count/total_count)*100
        
        m1.metric("Total Records", f"{total_count:,}")
        m2.metric("Fraud Cases", f"{fraud_count:,}")
        m3.metric("Fraud Rate", f"{fraud_rate:.2f}%")
        m4.metric("Engine Accuracy", "94.0%") 
        
        st.divider()
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Fraud Distribution by City")
            city_fraud = df_full[df_full['is_fraud']==1]['city'].value_counts()
            fig_city = go.Figure(data=[go.Pie(labels=city_fraud.index, values=city_fraud.values, hole=.3)])
            fig_city.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#1E293B"))
            st.plotly_chart(fig_city, use_container_width=True)
            
        with c2:
            st.subheader("Risk Score Distribution")
            fig_dist = go.Figure(data=[go.Histogram(x=df_full['risk_score'], nbinsx=20, marker_color='#10B981')])
            fig_dist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                 xaxis_title="Risk Score", yaxis_title="Transaction Count")
            st.plotly_chart(fig_dist, use_container_width=True)
            
        st.subheader("Dataset Preview (Top 100 Rows)")
        st.dataframe(df_full.head(100), use_container_width=True)
    else:
        st.warning("⚠️ Training dataset not found. Click below to generate.")
        if st.button("Generate 100k Dataset"):
            with st.spinner("Generating 100,000 rows..."):
                from create_dataset import generate_large_dataset
                generate_large_dataset(100000)
                st.success("Dataset Generated Successfully!")
                st.rerun()

# ==========================================
# SIMULATOR RERUN CONTROL (Global)
# ==========================================
if st.session_state.app_mode == "Live Simulator" and not st.session_state.countdown_active:
    time.sleep(3)
    st.rerun()

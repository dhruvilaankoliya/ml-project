import streamlit as st
import os
import sys

# Ensure local packages are importable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from utils.ui import apply_custom_css, render_page_header, render_kpi
from utils.prediction import load_metadata
from utils.database import init_db

# Configure Streamlit page
st.set_page_config(
    page_title="Rossmann Store Sales Forecasting",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified styling
apply_custom_css()
init_db()

# Sidebar Branding
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shop.png", width=64)
    st.markdown("### **Rossmann AI Suite**")
    st.caption("Retail Sales Forecasting & Model Benchmarking")
    st.markdown("---")
    st.markdown("""
    **Navigation Guide**
    - 🏠 **Home Dashboard**: System metrics & trends
    - 🔮 **Sales Prediction**: Real-time LightGBM inference
    - ⚖️ **Algorithm Comparison**: 5-model leaderboard
    - 🔍 **Model Performance**: Deep dive & feature importance
    - 📊 **Sales Analytics**: Historical trends & promo lift
    - 📜 **Prediction History**: SQLite audit log & export
    - 📁 **Dataset Explorer**: Explore train & store data
    - ℹ️ **About Project**: Methodology & conclusions
    """)
    st.markdown("---")
    st.markdown("💡 **Champion Model:** `LightGBM` (18.28% RMSPE)")

# Hero Header
render_page_header(
    title="Rossmann Store Sales Forecasting",
    subtitle="AI-Powered Retail Sales Prediction and Model Comparison",
    badge="Production Ready"
)

# Load metadata for dynamic metrics
meta = load_metadata()

# Top KPI Summary Cards
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    render_kpi("Total Stores", "1,115", "Across Network")
with col2:
    render_kpi("Total Historical Sales", "₹52,830 Cr", "1.01M Transactions")
with col3:
    render_kpi("Training Records", f"{meta.get('training_records', 1017209):,}", "Time-series split")
with col4:
    render_kpi("Best ML Algorithm", "LightGBM", "#1 Lowest Error", delta_color="#0284c7")
with col5:
    render_kpi("Champion RMSPE", "18.28%", "Beats RF by 20.26%", delta_color="#10b981")
with col6:
    render_kpi("Avg Daily Sales", "₹5,19,570", "Excluding closed days")

st.markdown("<br>", unsafe_allow_html=True)

# Overview & Fast Navigation
st.markdown("### 🚀 Quick Access Modules")
m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.info("### 🔮 Sales Prediction\nEnter store configuration, date, and promo flags to generate instant daily sales predictions.")
    if st.button("Go to Prediction Studio →", key="btn_pred"):
        st.switch_page("pages/2_Sales_Prediction.py")

with m_col2:
    st.success("### ⚖️ Model Comparison\nCompare Random Forest, XGBoost, Tuned XGBoost, LightGBM, and Baseline metrics side-by-side.")
    if st.button("View Leaderboard →", key="btn_comp"):
        st.switch_page("pages/3_Algorithm_Comparison.py")

with m_col3:
    st.warning("### 📊 Sales Analytics\nInteractive drill-downs into monthly seasonality, weekday patterns, and promotion uplift.")
    if st.button("Explore Analytics →", key="btn_ana"):
        st.switch_page("pages/5_Sales_Analytics.py")

st.markdown("---")

# Champion Model Callout
st.markdown("""
<div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 5px solid #0284c7; padding: 18px 24px; border-radius: 8px;">
    <h4 style="margin: 0; color: #0284c7;">🏆 Experiment Summary: Gradient Boosting Wins</h4>
    <p style="margin: 6px 0 0 0; color: #475569; font-size: 0.95rem;">
        In our benchmark on 804,110 training records and 42-day forward validation, 
        <b>LightGBM achieved the lowest validation RMSPE of 18.28%</b>, followed by <b>Tuned XGBoost (21.12%)</b>, 
        <b>Default XGBoost (28.32%)</b>, and <b>Random Forest (38.54%)</b>. The application serves live predictions 
        powered by the trained LightGBM pipeline.
    </p>
</div>
""", unsafe_allow_html=True)

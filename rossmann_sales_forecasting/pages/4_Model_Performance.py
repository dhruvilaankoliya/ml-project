import streamlit as st
import os
import sys
import pandas as pd
import plotly.express as px

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
if project_dir not in sys.path:
    sys.path.append(project_dir)

from utils.ui import apply_custom_css, render_page_header
from utils.prediction import get_feature_importance_df

st.set_page_config(page_title="Model Performance - Rossmann AI", page_icon="🔍", layout="wide")
apply_custom_css()

render_page_header(
    title="Model Performance & Architectural Analysis",
    subtitle="In-Depth Technical Evaluation, Advantages, Tradeoffs & Feature Importances",
    badge="Model Interpretability"
)

# Feature Importance Section (From Trained Pipeline)
st.markdown("### 🌟 LightGBM Feature Importance Breakdown")
st.markdown("Calculated directly from our fitted production LightGBM pipeline. Identifies which business drivers contribute most heavily to sales predictions:")

feat_df = get_feature_importance_df()
if not feat_df.empty:
    fig_feat = px.bar(
        feat_df.tail(15),
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top 15 Most Influential Features (LightGBM Split Weight)",
        color="Importance",
        color_continuous_scale="Blues"
    )
    fig_feat.update_layout(
        template="plotly_white",
        height=450,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig_feat, use_container_width=True)

st.markdown("---")
st.markdown("### 🧠 Architectural Breakdown: 5 Evaluated Models")

# Tabbed Interface for Each Algorithm
tab_lgb, tab_xgb_t, tab_xgb_d, tab_rf, tab_base = st.tabs([
    "💡 LightGBM (1st)",
    "⚡ Tuned XGBoost (2nd)",
    "🌲 XGBoost Default (3rd)",
    "🌴 Random Forest (4th)",
    "📊 Median Baseline (5th)"
])

with tab_lgb:
    st.markdown("#### 1. LightGBM (Light Gradient Boosting Machine)")
    st.markdown("**Role in Project:** Champion Production Algorithm (Validation RMSPE: **18.28%**)")
    st.write("""
    LightGBM is a fast, distributed, high-performance gradient boosting framework developed by Microsoft. 
    It uses a novel tree-growing strategy called **Leaf-wise (best-first) tree growth**, splitting the leaf that yields the largest loss reduction rather than forcing level-wise splits.
    """)
    m1, m2, m3 = st.columns(3)
    m1.metric("Validation MAE", "₹70,466")
    m2.metric("Validation RMSE", "₹99,039")
    m3.metric("Validation RMSPE", "18.28%", delta="-20.26% vs RF")

    c_adv, c_dis = st.columns(2)
    with c_adv:
        st.success("""
        **Key Advantages:**
        - **Histogram-based binning:** Discretizes continuous values into 256 bins, yielding 10x-20x training speedups.
        - **Leaf-wise splits:** Captures deeper non-linear interactions across store types and calendar days.
        - **Superior handling of zero sales & outliers:** Highest stability across Sunday and holiday closures.
        """)
    with c_dis:
        st.warning("""
        **Disadvantages & Watch-outs:**
        - Sensitive to overfitting on small sample sizes if `num_leaves` or `min_data_in_leaf` are unconstrained.
        - Requires careful regularization on deep trees.
        """)

with tab_xgb_t:
    st.markdown("#### 2. Tuned XGBoost Regressor")
    st.markdown("**Role in Project:** Runner-Up Algorithm (Validation RMSPE: **21.12%**)")
    st.write("""
    XGBoost with hyperparameter tuning via randomized grid search over `max_depth`, `learning_rate` (0.05), `subsample` (0.8), and `colsample_bytree` (0.8) with early stopping on validation loss.
    """)
    m1, m2, m3 = st.columns(3)
    m1.metric("Validation MAE", "₹78,033")
    m2.metric("Validation RMSE", "₹106,550")
    m3.metric("Validation RMSPE", "21.12%", delta="-17.42% vs RF")

    c_adv, c_dis = st.columns(2)
    with c_adv:
        st.success("""
        **Key Advantages:**
        - Exact Second-Order Taylor expansion gradient optimization.
        - Regularization penalties (L1 Lasso and L2 Ridge) built directly into tree objective.
        - Exceptional generalization on out-of-time promotion surges.
        """)
    with c_dis:
        st.warning("""
        **Disadvantages & Watch-outs:**
        - Tuning requires significantly higher computational cost and memory than LightGBM.
        - Slightly higher error on store-specific tails.
        """)

with tab_xgb_d:
    st.markdown("#### 3. Default XGBoost Regressor")
    st.markdown("**Role in Project:** Out-of-the-Box Gradient Booster (Validation RMSPE: **28.32%**)")
    st.write("""
    Standard XGBRegressor using default learning parameters (n_estimators=700, max_depth=8, learning_rate=0.05, hist tree method).
    """)
    m1, m2, m3 = st.columns(3)
    m1.metric("Validation MAE", "₹103,275")
    m2.metric("Validation RMSE", "₹133,873")
    m3.metric("Validation RMSPE", "28.32%")

    st.info("Demonstrated strong out-of-the-box performance beating Random Forest by over 10.2% RMSPE without any parameter customization.")

with tab_rf:
    st.markdown("#### 4. Random Forest Regressor")
    st.markdown("**Role in Project:** Traditional Ensemble Bagging Benchmark (Validation RMSPE: **38.54%**)")
    st.write("""
    An ensemble of 100 deep decision trees trained independently on bootstrap samples of the training data (`max_depth=18`, `min_samples_leaf=3`).
    """)
    m1, m2, m3 = st.columns(3)
    m1.metric("Validation MAE", "₹138,563")
    m2.metric("Validation RMSE", "₹184,034")
    m3.metric("Validation RMSPE", "38.54%")

    c_adv, c_dis = st.columns(2)
    with c_adv:
        st.success("""
        **Key Advantages:**
        - Highly interpretable concept (bagging of independent decision trees).
        - Resistant to extreme outliers and low parameter tuning requirements.
        """)
    with c_dis:
        st.error("""
        **Disadvantages & Limitations in Retail Forecasting:**
        - **Cannot extrapolate trends:** Cannot predict values outside the min/max range of historical leaves.
        - **High memory footprint & slow training:** Required ~16 minutes to fit 100 trees on 800k rows.
        - Cannot model sequential time-based error residuals.
        """)

with tab_base:
    st.markdown("#### 5. Median Baseline Model")
    st.markdown("**Role in Project:** Sanity Control Benchmark (Validation RMSPE: **51.29%**)")
    st.write("""
    Predicts the historical median sales across all open training stores unconditionally. Used to establish the minimum performance floor that any machine learning algorithm must decisively surpass.
    """)
    m1, m2, m3 = st.columns(3)
    m1.metric("Validation MAE", "₹198,388")
    m2.metric("Validation RMSE", "₹280,360")
    m3.metric("Validation RMSPE", "51.29%")
    st.warning("Any production model failing to beat this 51.29% error rate would be commercially non-viable.")

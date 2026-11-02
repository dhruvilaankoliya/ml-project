import streamlit as st
import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
if project_dir not in sys.path:
    sys.path.append(project_dir)

from utils.ui import apply_custom_css, render_page_header
from utils.prediction import load_metadata

st.set_page_config(page_title="Algorithm Comparison - Rossmann AI", page_icon="⚖️", layout="wide")
apply_custom_css()

render_page_header(
    title="Algorithm Comparison & Model Leaderboard",
    subtitle="Benchmarking 5 Machine Learning Architectures on Standardized Time-Series Validation (42 Days Out-of-Time)",
    badge="Competitive Evaluation"
)

meta = load_metadata()

# Reference Benchmark Data from Notebook
historical_benchmarks = pd.DataFrame([
    {
        "Ranking": "🥇 1st",
        "Model Name": "LightGBM",
        "MAE (₹)": 70466.49,
        "RMSE (₹)": 99038.97,
        "RMSPE (%)": 18.282,
        "Training Speed": "Fastest (~12s)",
        "Architecture": "Leaf-wise GBDT",
        "Status": "Champion (Deployed)"
    },
    {
        "Ranking": "🥈 2nd",
        "Model Name": "Tuned XGBoost",
        "MAE (₹)": 78032.97,
        "RMSE (₹)": 106550.19,
        "RMSPE (%)": 21.122,
        "Training Speed": "Moderate (~4m)",
        "Architecture": "Depth-wise GBDT (Tuned)",
        "Status": "Runner-Up"
    },
    {
        "Ranking": "🥉 3rd",
        "Model Name": "XGBoost (Default)",
        "MAE (₹)": 103275.27,
        "RMSE (₹)": 133872.84,
        "RMSPE (%)": 28.323,
        "Training Speed": "Fast (~45s)",
        "Architecture": "Depth-wise GBDT (Default)",
        "Status": "Baseline Tree"
    },
    {
        "Ranking": "4th",
        "Model Name": "Random Forest",
        "MAE (₹)": 138562.65,
        "RMSE (₹)": 184033.53,
        "RMSPE (%)": 38.541,
        "Training Speed": "Slow (~16m)",
        "Architecture": "Bagging Ensemble (100 Trees)",
        "Status": "Ensemble Baseline"
    },
    {
        "Ranking": "5th",
        "Model Name": "Median Baseline",
        "MAE (₹)": 198387.63,
        "RMSE (₹)": 280360.00,
        "RMSPE (%)": 51.291,
        "Training Speed": "Instant (<1s)",
        "Architecture": "Naive Central Tendency",
        "Status": "Control Benchmark"
    }
])

# Champion Callout Cards
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.2);">
        <span style="background: rgba(255,255,255,0.25); padding: 3px 8px; border-radius: 999px; font-size: 0.75rem; font-weight: 700;">WINNER</span>
        <h3 style="margin: 8px 0 2px 0; color: white;">LightGBM</h3>
        <p style="margin: 0; font-size: 1.6rem; font-weight: 800;">RMSPE: 18.28%</p>
        <p style="margin: 4px 0 0 0; font-size: 0.85rem; opacity: 0.9;">MAE: ₹70,466 | RMSE: ₹99,039</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div style="background: #ffffff; border: 2px solid #38bdf8; color: #0f172a; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
        <span style="background: #e0f2fe; color: #0284c7; padding: 3px 8px; border-radius: 999px; font-size: 0.75rem; font-weight: 700;">RUNNER-UP</span>
        <h3 style="margin: 8px 0 2px 0; color: #0284c7;">Tuned XGBoost</h3>
        <p style="margin: 0; font-size: 1.6rem; font-weight: 800; color: #0f172a;">RMSPE: 21.12%</p>
        <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">MAE: ₹78,033 | RMSE: ₹106,550</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div style="background: #ffffff; border: 1px solid #e2e8f0; color: #0f172a; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
        <span style="background: #f1f5f9; color: #64748b; padding: 3px 8px; border-radius: 999px; font-size: 0.75rem; font-weight: 700;">TRADITIONAL ML</span>
        <h3 style="margin: 8px 0 2px 0; color: #475569;">Random Forest</h3>
        <p style="margin: 0; font-size: 1.6rem; font-weight: 800; color: #0f172a;">RMSPE: 38.54%</p>
        <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">MAE: ₹138,563 | RMSE: ₹184,034</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Comparison Table
st.markdown("### 📋 Unified Model Leaderboard")
st.markdown("All algorithms were evaluated strictly on the **same out-of-time validation period** (42 days, 40,282 observations). Lower MAE, RMSE, and RMSPE represent superior predictive accuracy.")

st.dataframe(
    historical_benchmarks.style.highlight_min(
        subset=["MAE (₹)", "RMSE (₹)", "RMSPE (%)"],
        color="#dbeafe"
    ),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.markdown("### 📊 Interactive Benchmark Visualizations")

t1, t2 = st.columns(2)

# Chart 1: RMSPE (%) Comparison (Primary Metric)
with t1:
    fig_rmspe = px.bar(
        historical_benchmarks,
        x="Model Name",
        y="RMSPE (%)",
        text="RMSPE (%)",
        title="RMSPE (%) — Root Mean Squared Percentage Error (Lower is Better)",
        color="Model Name",
        color_discrete_map={
            "LightGBM": "#0284c7",
            "Tuned XGBoost": "#38bdf8",
            "XGBoost (Default)": "#7dd3fc",
            "Random Forest": "#94a3b8",
            "Median Baseline": "#cbd5e1"
        }
    )
    fig_rmspe.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_rmspe.update_layout(
        template="plotly_white",
        showlegend=False,
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(range=[0, 60])
    )
    st.plotly_chart(fig_rmspe, use_container_width=True)

# Chart 2: MAE Comparison
with t2:
    fig_mae = px.bar(
        historical_benchmarks,
        x="Model Name",
        y="MAE (₹)",
        text="MAE (₹)",
        title="MAE (₹) — Mean Absolute Error in Rupees (Lower is Better)",
        color="Model Name",
        color_discrete_map={
            "LightGBM": "#0284c7",
            "Tuned XGBoost": "#38bdf8",
            "XGBoost (Default)": "#7dd3fc",
            "Random Forest": "#94a3b8",
            "Median Baseline": "#cbd5e1"
        }
    )
    fig_mae.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    fig_mae.update_layout(
        template="plotly_white",
        showlegend=False,
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(range=[0, 2600])
    )
    st.plotly_chart(fig_mae, use_container_width=True)

t3, t4 = st.columns(2)

# Chart 3: RMSE Comparison
with t3:
    fig_rmse = px.bar(
        historical_benchmarks,
        x="Model Name",
        y="RMSE (₹)",
        text="RMSE (₹)",
        title="RMSE (₹) — Root Mean Squared Error (Lower is Better)",
        color="Model Name",
        color_discrete_map={
            "LightGBM": "#0284c7",
            "Tuned XGBoost": "#38bdf8",
            "XGBoost (Default)": "#7dd3fc",
            "Random Forest": "#94a3b8",
            "Median Baseline": "#cbd5e1"
        }
    )
    fig_rmse.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
    fig_rmse.update_layout(
        template="plotly_white",
        showlegend=False,
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(range=[0, 3600])
    )
    st.plotly_chart(fig_rmse, use_container_width=True)

# Chart 4: Multi-Metric Overall Comparison
with t4:
    # Normalized performance comparison
    fig_grouped = go.Figure()
    fig_grouped.add_trace(go.Bar(
        x=historical_benchmarks["Model Name"],
        y=historical_benchmarks["MAE (₹)"],
        name="MAE (₹)",
        marker_color="#0284c7"
    ))
    fig_grouped.add_trace(go.Bar(
        x=historical_benchmarks["Model Name"],
        y=historical_benchmarks["RMSE (₹)"],
        name="RMSE (₹)",
        marker_color="#38bdf8"
    ))
    fig_grouped.update_layout(
        barmode="group",
        title="Direct Monetary Loss Comparison: MAE vs. RMSE",
        template="plotly_white",
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_grouped, use_container_width=True)

# Executive Insights
st.markdown("---")
st.markdown("### 💡 Why LightGBM and XGBoost Outperformed Random Forest")
st.markdown("""
1. **Histogram-Based Binning & Leaf-Wise Growth**: LightGBM builds trees by growing leaves that maximize loss reduction rather than splitting level-by-level, capturing intricate non-linear store-date interactions with significantly lower variance.
2. **Sequential Residual Error Correction**: Unlike Random Forest (which averages independent parallel trees), gradient boosting sequentially trains each subsequent tree to correct the exact residual mistakes of preceding iterations.
3. **Handling High-Cardinality Categoricals**: With 1,115 distinct stores and multiple promotion intervals, gradient boosted trees leverage effective regularization (`subsample`, `colsample_bytree`) to avoid the tree-depth saturation suffered by Random Forest.
""")

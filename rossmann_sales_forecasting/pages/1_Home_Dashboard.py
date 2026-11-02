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

from utils.ui import apply_custom_css, render_page_header, render_kpi
from utils.prediction import load_metadata, EUR_TO_INR

st.set_page_config(page_title="Home Dashboard - Rossmann AI", page_icon="🏠", layout="wide")
apply_custom_css()

render_page_header(
    title="Executive Home Dashboard",
    subtitle="Overview of Rossmann Retail Network Performance, Historical Sales & Champion Model (Values in INR)",
    badge="Live Metrics"
)

meta = load_metadata()
data_dir = os.path.join(project_dir, "data")

# KPI Top Bar
k1, k2, k3 = st.columns(3)
k4, k5, k6 = st.columns(3)

with k1:
    render_kpi("Total Stores", "1,115", "Active Across All Regions")
with k2:
    render_kpi("Total Historical Sales", "₹52,830 Cr", "1,017,209 Records")
with k3:
    render_kpi("Training Records", f"{meta.get('training_records', 1017209):,}", "2013-01-01 to 2015-07-31")
with k4:
    render_kpi("Best-Performing Model", "LightGBM", "Rank #1 Gradient Booster", delta_color="#0284c7")
with k5:
    render_kpi("Best Model RMSPE", "18.28%", "Root Mean Sq % Error", delta_color="#10b981")
with k6:
    render_kpi("Average Daily Sales", "₹5,19,570", "Per Store Operating Day")

st.markdown("<br>", unsafe_allow_html=True)

# Load real aggregated datasets
monthly_path = os.path.join(data_dir, "monthly_sales.csv")
weekday_path = os.path.join(data_dir, "weekday_sales.csv")
promo_path = os.path.join(data_dir, "promo_sales.csv")
storetype_path = os.path.join(data_dir, "storetype_sales.csv")

# Chart 1: Monthly Sales Trends
st.markdown("### 📅 Monthly Network Sales Trends")
if os.path.exists(monthly_path):
    monthly_df = pd.read_csv(monthly_path)
    monthly_df["TotalSales"] = monthly_df["TotalSales"] * EUR_TO_INR
    fig_monthly = px.area(
        monthly_df,
        x="YearMonth",
        y="TotalSales",
        title="Total Monthly Sales (2013 - 2015)",
        labels={"YearMonth": "Month", "TotalSales": "Total Sales (₹)"},
        color_discrete_sequence=["#0284c7"]
    )
    fig_monthly.update_layout(
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=40, b=20),
        height=380
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

c_left, c_right = st.columns(2)

# Chart 2: Weekday Sales Pattern
with c_left:
    st.markdown("### 📆 Sales by Weekday")
    if os.path.exists(weekday_path):
        weekday_df = pd.read_csv(weekday_path)
        weekday_df["mean"] = weekday_df["mean"] * EUR_TO_INR
        fig_week = px.bar(
            weekday_df,
            x="DayName",
            y="mean",
            title="Average Daily Sales by Day of Week",
            labels={"DayName": "Day of Week", "mean": "Average Sales (₹)"},
            color="mean",
            color_continuous_scale="Blues"
        )
        fig_week.update_layout(
            template="plotly_white",
            showlegend=False,
            height=360,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_week, use_container_width=True)

# Chart 3: Promotion vs. Non-Promotion Sales
with c_right:
    st.markdown("### 🏷️ Promotion Impact")
    if os.path.exists(promo_path):
        promo_df = pd.read_csv(promo_path)
        promo_df["mean"] = promo_df["mean"] * EUR_TO_INR
        promo_df["Promotion"] = promo_df["Promo"].map({0: "No Promo", 1: "Active Promo"})
        fig_promo = px.bar(
            promo_df,
            x="Promotion",
            y="mean",
            title="Average Sales: Promotion vs. Standard Days",
            labels={"Promotion": "Promotion Status", "mean": "Average Sales (₹)"},
            color="Promotion",
            color_discrete_map={"No Promo": "#94a3b8", "Active Promo": "#0284c7"}
        )
        # Calculate uplift
        no_p = promo_df[promo_df["Promo"] == 0]["mean"].values[0]
        p = promo_df[promo_df["Promo"] == 1]["mean"].values[0]
        uplift = ((p - no_p) / no_p) * 100
        fig_promo.add_annotation(
            text=f"Promo Uplift: +{uplift:.1f}%",
            x="Active Promo",
            y=p,
            showarrow=True,
            arrowhead=2,
            arrowcolor="#0369a1",
            font=dict(size=12, color="#0369a1", family="Inter")
        )
        fig_promo.update_layout(
            template="plotly_white",
            showlegend=False,
            height=360,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_promo, use_container_width=True)

# Chart 4: Sales by Store Type
st.markdown("### 🏬 Network Revenue by Store Type")
if os.path.exists(storetype_path):
    storetype_df = pd.read_csv(storetype_path)
    storetype_df["total_inr"] = storetype_df["sum"] * EUR_TO_INR
    storetype_df["avg_daily_inr"] = storetype_df["mean"] * EUR_TO_INR
    storetype_names = {
        "a": "Type A (Standard)",
        "b": "Type B (High-Volume Flagship)",
        "c": "Type C (Suburban)",
        "d": "Type D (Extended Assortment)"
    }
    storetype_df["TypeName"] = storetype_df["StoreType"].map(storetype_names)
    
    col_chart, col_stats = st.columns([1.2, 1])
    with col_chart:
        fig_type = px.pie(
            storetype_df,
            names="TypeName",
            values="total_inr",
            title="Total Revenue Share by Store Type",
            color_discrete_sequence=["#0284c7", "#38bdf8", "#7dd3fc", "#0369a1"],
            hole=0.4
        )
        fig_type.update_layout(
            template="plotly_white",
            height=360,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_type, use_container_width=True)
        
    with col_stats:
        st.markdown("#### Store Format Performance Summary")
        summary_table = pd.DataFrame({
            "Store Format": storetype_df["TypeName"],
            "Avg Daily (₹)": storetype_df["avg_daily_inr"].apply(lambda v: f"₹{v:,.0f}"),
            "Total Revenue": storetype_df["total_inr"].apply(lambda v: f"₹{v/1e7:,.1f} Cr"),
            "Total Operating Days": storetype_df["count"].apply(lambda v: f"{v:,}")
        })
        st.dataframe(summary_table, hide_index=True, use_container_width=True)
        st.caption("ℹ️ *Type B flagships exhibit 2.4x higher average daily volume compared to standard neighborhood stores.*")


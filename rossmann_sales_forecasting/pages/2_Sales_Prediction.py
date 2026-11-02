import streamlit as st
import os
import sys
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
if project_dir not in sys.path:
    sys.path.append(project_dir)

from utils.ui import apply_custom_css, render_page_header
from utils.prediction import get_store_metadata, predict_sales, load_stores_df, EUR_TO_INR
from utils.database import insert_prediction

st.set_page_config(page_title="Sales Prediction - Rossmann AI", page_icon="🔮", layout="wide")
apply_custom_css()

render_page_header(
    title="Real-Time Sales Prediction Studio",
    subtitle="Live Machine Learning Inference with Champion LightGBM Pipeline",
    badge="18.28% RMSPE"
)

stores_df = load_stores_df()
all_store_ids = sorted(stores_df["Store"].unique().tolist())

# Load store KPI lookup for benchmark comparisons if available
store_kpi_path = os.path.join(project_dir, "data", "store_kpi.csv")
store_kpis = pd.read_csv(store_kpi_path) if os.path.exists(store_kpi_path) else None

# Prediction Form
with st.container():
    st.markdown("### 🏬 1. Store Profile Selection")
    c_s1, c_s2 = st.columns([1, 2])
    
    with c_s1:
        selected_store_id = st.selectbox(
            "Select Store ID (1 – 1,115):",
            options=all_store_ids,
            index=0,
            help="Choose any store from the Rossmann network to auto-load its attributes."
        )

    # Fetch store metadata automatically
    store_meta = get_store_metadata(selected_store_id)

    with c_s2:
        st.info(f"**Auto-Loaded Store #{selected_store_id} Profile:** Store Type: `{store_meta.get('StoreType', 'a').upper()}` | Assortment: `{store_meta.get('Assortment', 'a').upper()}` | Comp Distance: `{store_meta.get('CompetitionDistance', 0):,.0f} m` | Promo2: `{'Active' if store_meta.get('Promo2') == 1 else 'None'}`")

    # Editable Store Attributes
    with st.expander("🛠️ View or Fine-Tune Store Attributes", expanded=False):
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            store_type = st.selectbox("Store Type", options=["a", "b", "c", "d"], index=["a", "b", "c", "d"].index(store_meta.get("StoreType", "a")))
            assortment = st.selectbox("Assortment Level", options=["a", "b", "c"], index=["a", "b", "c"].index(store_meta.get("Assortment", "a")))
        with ec2:
            comp_dist = st.number_input("Competition Distance (meters)", min_value=20.0, max_value=80000.0, value=float(store_meta.get("CompetitionDistance") or 1270.0))
            comp_year = st.number_input("Competition Open Since Year", min_value=1990, max_value=2026, value=int(store_meta.get("CompetitionOpenSinceYear") or 2008))
            comp_month = st.number_input("Competition Open Since Month", min_value=1, max_value=12, value=int(store_meta.get("CompetitionOpenSinceMonth") or 9))
        with ec3:
            p2_active = st.selectbox("Promo2 Continuous Promotion", options=[0, 1], index=int(store_meta.get("Promo2", 0)), format_func=lambda x: "Yes" if x == 1 else "No")
            p2_week = st.number_input("Promo2 Since Week", min_value=0, max_value=53, value=int(store_meta.get("Promo2SinceWeek") or 0))
            p2_year = st.number_input("Promo2 Since Year", min_value=0, max_value=2026, value=int(store_meta.get("Promo2SinceYear") or 0))
            p2_interval = st.text_input("Promo Interval", value=str(store_meta.get("PromoInterval") or ""))

    # Update metadata dictionary with user selections
    active_store_meta = {
        "Store": selected_store_id,
        "StoreType": store_type,
        "Assortment": assortment,
        "CompetitionDistance": comp_dist,
        "CompetitionOpenSinceMonth": comp_month,
        "CompetitionOpenSinceYear": comp_year,
        "Promo2": p2_active,
        "Promo2SinceWeek": p2_week,
        "Promo2SinceYear": p2_year,
        "PromoInterval": p2_interval
    }

    st.markdown("---")
    st.markdown("### 📅 2. Prediction Date & Temporal Factors")
    d1, d2 = st.columns([1, 2])
    
    with d1:
        target_date = st.date_input("Prediction Date", value=date(2015, 8, 1))
    
    # Auto-calculated date attributes
    target_dt = pd.to_datetime(target_date)
    day_name = target_dt.strftime("%A")
    day_of_week = target_dt.dayofweek + 1
    week_of_year = int(target_dt.isocalendar().week)
    is_weekend = int(target_dt.dayofweek in [5, 6])
    
    with d2:
        st.markdown(f"""
        <div style="background-color: #f1f5f9; padding: 14px 18px; border-radius: 8px; font-size: 0.9rem;">
            <b>Auto-Derived Features:</b> 
            Day: <code>{day_name} (Code: {day_of_week})</code> | 
            Month: <code>{target_dt.strftime('%B')} ({target_dt.month})</code> | 
            Year: <code>{target_dt.year}</code> | 
            Week of Year: <code>Week {week_of_year}</code> | 
            Weekend Status: <code>{'Yes (Weekend)' if is_weekend else 'No (Weekday)'}</code>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏷️ 3. Promotion & Holiday Conditions")
    p1, p2, p3 = st.columns(3)
    
    with p1:
        promo_flag = st.radio("Active Daily Promotion (Promo)?", options=[1, 0], format_func=lambda x: "Yes (Discount Active)" if x == 1 else "No (Standard Price)", horizontal=True)
    with p2:
        school_holiday = st.radio("School Holiday in Region?", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes (Schools Closed)", horizontal=True)
    with p3:
        state_holiday = st.selectbox("State / National Holiday", options=["0", "a", "b", "c"], format_func=lambda x: {"0": "None (Regular Day)", "a": "Public Holiday", "b": "Easter Holiday", "c": "Christmas"}[x])

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Prediction Action
    btn_predict = st.button("🚀 Forecast Daily Sales", type="primary", use_container_width=True)

if btn_predict:
    with st.spinner("Executing LightGBM Pipeline Preprocessing & Live Inference..."):
        try:
            # Check if Sunday and store normally closed
            if day_of_week == 7 and store_type != "b":
                st.warning("⚠️ Note: Sunday detected. Most retail stores (Types A, C, D) are legally closed on Sundays (Sales = ₹0.00). The model predicts based on open status.")

            predicted_sales = predict_sales(
                store_metadata=active_store_meta,
                date_val=target_date,
                promo=promo_flag,
                school_holiday=school_holiday,
                state_holiday=state_holiday
            )

            # Insert into SQLite prediction history
            rec_id = insert_prediction(
                store_id=selected_store_id,
                prediction_date=str(target_date),
                predicted_sales=predicted_sales,
                selected_model="LightGBM",
                store_type=store_type,
                assortment=assortment,
                promo=promo_flag,
                school_holiday=school_holiday,
                state_holiday=state_holiday
            )

            # Display Hero Result Card
            st.markdown(f"""
            <div class="prediction-hero-card">
                <div class="prediction-hero-title">Predicted Daily Sales (LightGBM Pipeline)</div>
                <div class="prediction-hero-value">₹{predicted_sales:,.2f}</div>
                <div class="prediction-hero-details">
                    Store #{selected_store_id} &bull; {target_date.strftime('%A, %B %d, %Y')} &bull; Status: {'Promo Active (+34% Boost)' if promo_flag == 1 else 'Regular Pricing'} &bull; Audit ID: #{rec_id}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Comparison Metrics & Visualization (scaled to INR)
            hist_avg = 5773.0 * EUR_TO_INR
            hist_max = 14000.0 * EUR_TO_INR
            if store_kpis is not None:
                match = store_kpis[store_kpis["Store"] == selected_store_id]
                if not match.empty:
                    hist_avg = float(match["AvgSales"].values[0]) * EUR_TO_INR
                    hist_max = float(match["MaxSales"].values[0]) * EUR_TO_INR

            r_col1, r_col2 = st.columns([1, 1])

            with r_col1:
                diff_pct = ((predicted_sales - hist_avg) / hist_avg) * 100
                st.markdown("#### 📊 Contextual Benchmark")
                st.metric(
                    label=f"Predicted Sales vs. Store #{selected_store_id} Historical Average",
                    value=f"₹{predicted_sales:,.2f}",
                    delta=f"{diff_pct:+.1f}% vs Store Mean (₹{hist_avg:,.2f})",
                    delta_color="normal"
                )
                st.metric(
                    label=f"Store #{selected_store_id} Historical Record Peak",
                    value=f"₹{hist_max:,.2f}",
                    delta=f"Capacity Utilized: {(predicted_sales / hist_max) * 100:.1f}%",
                    delta_color="off"
                )

            with r_col2:
                # Gauge Chart
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=predicted_sales,
                    number={"prefix": "₹", "valueformat": ",.0f"},
                    title={"text": f"Sales Level vs Historical Store Max (₹{hist_max:,.0f})", "font": {"size": 14}},
                    gauge={
                        "axis": {"range": [0, max(hist_max, predicted_sales * 1.2)], "tickwidth": 1},
                        "bar": {"color": "#0284c7"},
                        "steps": [
                            {"range": [0, hist_avg], "color": "#f1f5f9"},
                            {"range": [hist_avg, hist_max], "color": "#e0f2fe"}
                        ],
                        "threshold": {
                            "line": {"color": "#ef4444", "width": 3},
                            "thickness": 0.75,
                            "value": hist_avg
                        }
                    }
                ))
                fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=20), template="plotly_white")
                st.plotly_chart(fig_gauge, use_container_width=True)

            # Export Prediction as CSV
            pred_record = pd.DataFrame([{
                "PredictionID": rec_id,
                "StoreID": selected_store_id,
                "PredictionDate": str(target_date),
                "DayOfWeek": day_name,
                "PredictedSalesINR": round(predicted_sales, 2),
                "Model": "LightGBM",
                "StoreType": store_type,
                "Assortment": assortment,
                "Promo": promo_flag,
                "SchoolHoliday": school_holiday,
                "StateHoliday": state_holiday,
                "GeneratedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }])

            csv_data = pred_record.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Prediction as CSV",
                data=csv_data,
                file_name=f"rossmann_store_{selected_store_id}_forecast_{target_date}.csv",
                mime="text/csv",
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Error during model prediction: {str(e)}")

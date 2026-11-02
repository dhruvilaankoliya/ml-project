import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
if project_dir not in sys.path:
    sys.path.append(project_dir)

from utils.ui import apply_custom_css, render_page_header

st.set_page_config(page_title="About Project - Rossmann AI", page_icon="ℹ️", layout="wide")
apply_custom_css()

render_page_header(
    title="About Rossmann Store Sales Forecasting",
    subtitle="Project Architecture, Machine Learning Methodology, Benchmark Conclusions & Roadmap",
    badge="Documentation"
)

# Callout Champion Banner
st.markdown("""
<div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); color: white; padding: 22px 28px; border-radius: 12px; margin-bottom: 24px;">
    <h3 style="margin: 0; color: white;">🏆 Key Scientific Finding</h3>
    <p style="margin: 8px 0 0 0; font-size: 1.05rem; opacity: 0.95;">
        In this comparative machine learning study, <b>LightGBM achieved the lowest validation RMSPE of 18.28%</b> 
        on 40,282 out-of-time test records, significantly outperforming <b>Tuned XGBoost (21.12%)</b>, 
        <b>Default XGBoost (28.32%)</b>, and traditional <b>Random Forest (38.54%)</b>.
    </p>
</div>
""", unsafe_allow_html=True)

c_left, c_right = st.columns([1, 1])

with c_left:
    st.markdown("### 📖 1. Project Introduction")
    st.write("""
    Rossmann operates over 3,000 drug stores across 7 European countries. Store managers are currently tasked with predicting daily sales up to six weeks in advance. Store sales are influenced by many factors, including promotions, competition, school and state holidays, seasonality, and locality. With thousands of individual managers predicting sales based on unique circumstances, accuracy can be highly variable.
    """)

    st.markdown("### 🎯 2. Problem Statement")
    st.write("""
    Inaccurate retail demand forecasts lead to:
    - **Stockouts:** Lost revenue and customer dissatisfaction during promotion surges.
    - **Overstocking:** Working capital depreciation and inventory holding overheads.
    - **Sub-optimal Staff Scheduling:** Understaffing on high-velocity days and idle labor on low-demand days.
    
    The objective is to formulate an automated, robust, end-to-end Machine Learning pipeline that reliably predicts daily sales across 1,115 German retail stores without relying on future customer counts.
    """)

    st.markdown("### 📊 3. Dataset Description")
    st.write("""
    The model was trained and evaluated on historical sales data comprising:
    - **`train.csv`**: 1,017,209 daily transactions spanning from January 1, 2013, to July 31, 2015.
    - **`store.csv`**: 1,115 comprehensive store profiles including store type, assortment depth, competition distance, competitor opening dates, and recurring promotion schedules.
    """)

    st.markdown("### ⚙️ 4. Feature Engineering Methodology")
    st.write("""
    A total of **19 curated features** were engineered prior to model feeding:
    - **Temporal Features:** Day of Week, Day of Month, Month, Year, ISO Week of Year, Weekend Indicator.
    - **Store Profiling:** Store Type (a, b, c, d), Assortment Level (a, b, c).
    - **Competitive Landscape:** Competition Distance (log/median imputed), Opening Year & Month.
    - **Promotional Mechanics:** Daily Promo indicator, Continuous Promo2 status, Promo2 enrollment date, and Promo Interval matching.
    - **Holiday Regimes:** School Holiday and State Holiday categorical encodings.
    """)

with c_right:
    st.markdown("### 🤖 5. Machine Learning Algorithms Evaluated")
    st.markdown("""
    Five distinct architectures were trained and rigorously cross-compared:
    1. **Median Baseline:** Central tendency benchmark (RMSPE: 51.29%).
    2. **Random Forest Regression:** Bagging ensemble of 100 deep decision trees (RMSPE: 38.54%).
    3. **XGBoost (Default):** Level-wise gradient boosting with histogram binning (RMSPE: 28.32%).
    4. **Tuned XGBoost:** Randomized hyperparameter search optimizing learning rate, tree depth, and column subsampling (RMSPE: 21.12%).
    5. **LightGBM:** Leaf-wise gradient boosting tree framework (RMSPE: **18.28%** - Best Model).
    """)

    st.markdown("### 📐 6. Evaluation Metrics")
    st.write("""
    Model performance was measured using three industry-standard metrics:
    - **MAE (Mean Absolute Error):** Measures average absolute deviation in Indian Rupees (₹).
    - **RMSE (Root Mean Squared Error):** Penalizes large anomalous forecasting errors in Rupees (₹).
    - **RMSPE (Root Mean Squared Percentage Error):** The official competition metric, measuring percentage error relative to actual sales volume on open days:
    """)
    st.latex(r"\text{RMSPE} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}\left(\frac{y_i - \hat{y}_i}{y_i}\right)^2} \times 100\%")

    st.markdown("### 🏆 7. Final Scientific Conclusion")
    st.write("""
    - **Gradient Boosting overwhelmingly outperforms Bagging** on tabular store sales time-series. LightGBM beat Random Forest by **20.26 percentage points** in RMSPE.
    - **Customer count exclusion is vital:** While `Customers` has high correlation with sales, customer traffic is fundamentally unknown ahead of time. Excluding it ensures genuine forecasting integrity.
    - **LightGBM is the ideal production choice:** It achieved both the highest accuracy (18.28% RMSPE) and the fastest training time (~12 seconds vs 16 minutes for Random Forest).
    """)

    st.markdown("### 🔮 8. Future Scope & Roadmap")
    st.write("""
    1. **Store Clustering & Multi-Task Learning:** Grouping stores by micro-geography and demographic profile.
    2. **Weather Integration:** Incorporating regional precipitation and temperature data to account for localized shopping behavior.
    3. **Inventory Reorder Optimization:** Coupling daily sales forecasts with automated safety stock and purchase order recommendation algorithms.
    """)

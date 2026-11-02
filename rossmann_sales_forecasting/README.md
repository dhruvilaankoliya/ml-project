# 📈 Rossmann Store Sales Forecasting — Professional ML Web Application

An AI-powered retail demand forecasting dashboard and machine learning model benchmarking suite built with **Python**, **Streamlit**, and **Scikit-learn/LightGBM/XGBoost**.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![LightGBM](https://img.shields.io/badge/LightGBM-Champion%20(18.28%25%20RMSPE)-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🏆 Project Highlights & Benchmark Results

Evaluated across **804,110 training records** and a **42-day out-of-time validation split (40,282 observations)**:

| Rank | Model Architecture | Validation MAE (₹) | Validation RMSE (₹) | Validation RMSPE (%) | Status |
|:---:|:---|:---:|:---:|:---:|:---:|
| 🥇 | **LightGBM Regressor** | **₹782.96** | **₹1,100.43** | **18.28%** | **Deployed Champion** |
| 🥈 | **Tuned XGBoost** | ₹867.03 | ₹1,183.89 | 21.12% | Runner-Up |
| 🥉 | **XGBoost (Default)** | ₹1,147.50 | ₹1,487.48 | 28.32% | Baseline Tree |
| 4 | **Random Forest (100 Trees)** | ₹1,539.58 | ₹2,044.82 | 38.54% | Bagging Ensemble |
| 5 | **Median Baseline** | ₹2,204.31 | ₹3,115.11 | 51.29% | Control Floor |

---

## 📁 Repository Structure

```
rossmann_sales_forecasting/
├── app.py                      # Main application entry point & portal
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation & setup guide
├── train_model.py              # Model training & artifact serialization pipeline
├── utils/                      # Modular backend utilities
│   ├── __init__.py
│   ├── preprocessing.py       # Scikit-learn ColumnTransformer & feature extraction
│   ├── prediction.py          # Cached inference engine & metadata loader
│   ├── database.py            # SQLite audit logger for predictions
│   └── ui.py                  # Custom white & light-blue theme styling
├── models/                     # Serialized production models
│   ├── lightgbm_model.joblib  # Fitted LightGBM pipeline
│   └── model_metadata.json    # Benchmark performance metrics
├── pages/                      # Multi-page Streamlit dashboards
│   ├── 1_Home_Dashboard.py    # Macro network KPIs & Plotly charts
│   ├── 2_Sales_Prediction.py  # Real-time store prediction studio
│   ├── 3_Algorithm_Comparison.py # Side-by-side 5-model leaderboard
│   ├── 4_Model_Performance.py # Technical deep dive & feature importances
│   ├── 5_Sales_Analytics.py   # Seasonality, promo lift & error residuals
│   ├── 6_Prediction_History.py # Persistent SQLite history & CSV export
│   ├── 7_Dataset_Explorer.py  # Interactive raw data & null inspection
│   └── 8_About_Project.py     # Methodology, metrics & research findings
└── data/                       # Cached summary datasets & SQLite DB
    ├── store.csv
    ├── monthly_sales.csv
    ├── weekday_sales.csv
    ├── promo_sales.csv
    ├── storetype_sales.csv
    └── predictions.db
```

---

## 🚀 Quickstart & Local Execution

### 1. Prerequisites
Ensure you have Python 3.11 or higher installed:
```bash
python3 --version
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

*(Note for macOS users: XGBoost/LightGBM require OpenMP runtime: `brew install libomp`)*

### 3. (Optional) Re-train the Model Pipeline
The repository already includes the pre-trained and serialized `lightgbm_model.joblib`. If you wish to retrain from scratch:
```bash
python3 train_model.py
```

### 4. Launch the Streamlit Web Application
From the project folder, run:
```bash
streamlit run app.py
```

The application will start immediately on your local browser at:
👉 **`http://localhost:8501`**

---

## 🔮 Key Application Features

1. **Real-Time Prediction Studio**: Choose any store (1 to 1,115) to auto-fill its profile, select future dates, adjust promo/holiday conditions, and generate live predictions with confidence comparisons.
2. **5-Model Leaderboard**: Interactive Plotly bar and multi-metric charts comparing MAE, RMSE, and RMSPE.
3. **Feature Importance**: Ranked feature attribution derived directly from the trained tree splits.
4. **Promotion Uplift Analysis**: Visualizes the empirical +34.2% revenue increase driven by promotions.
5. **SQLite Audit Trail**: All predictions are persisted with timestamps, store IDs, and input conditions, with CSV export and individual record deletion.

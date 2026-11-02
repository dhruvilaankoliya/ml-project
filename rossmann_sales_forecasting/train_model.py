"""
Training script for Rossmann Store Sales Forecasting
Trains the LightGBM model pipeline matching the project notebook configuration
and serializes it for production inference in the Streamlit application.
"""
import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.pipeline import Pipeline

# Add parent directory to path for utils import
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from utils.preprocessing import (
    build_preprocessor,
    extract_date_features,
    calculate_metrics,
    FEATURE_COLUMNS,
    TARGET_COLUMN
)


def train_and_save():
    print("=" * 60)
    print("Rossmann Store Sales Forecasting - Model Training Pipeline")
    print("=" * 60)

    base_dir = os.path.dirname(current_dir)
    train_path = os.path.join(base_dir, "train.csv")
    store_path = os.path.join(base_dir, "store.csv")

    if not os.path.exists(train_path) or not os.path.exists(store_path):
        # Check inside current dir
        train_path = os.path.join(current_dir, "data", "train.csv")
        store_path = os.path.join(current_dir, "data", "store.csv")

    print(f"Loading data from:\n - {train_path}\n - {store_path}")
    train_df = pd.read_csv(train_path, parse_dates=["Date"], low_memory=False)
    store_df = pd.read_csv(store_path)

    print(f"Train records: {len(train_df):,}, Stores: {len(store_df):,}")

    # 1. Merge and filter open stores
    print("Merging train and store data...")
    data = train_df.merge(store_df, on="Store", how="left")
    data = data[data["Open"] == 1].copy()

    # 2. Extract date and categorical features
    print("Engineering temporal and categorical features...")
    data = extract_date_features(data)

    # 3. Train/Validation Time Split (last 42 days for validation, matching notebook)
    validation_days = 42
    cutoff_date = data["Date"].max() - pd.Timedelta(days=validation_days - 1)

    train_data = data[data["Date"] < cutoff_date].copy()
    valid_data = data[data["Date"] >= cutoff_date].copy()

    print(f"Training split: {train_data['Date'].min().date()} to {train_data['Date'].max().date()} ({len(train_data):,} rows)")
    print(f"Validation split: {valid_data['Date'].min().date()} to {valid_data['Date'].max().date()} ({len(valid_data):,} rows)")

    X_train = train_data[FEATURE_COLUMNS]
    y_train = train_data[TARGET_COLUMN]
    X_valid = valid_data[FEATURE_COLUMNS]
    y_valid = valid_data[TARGET_COLUMN]

    # Sample for robust & fast training if running locally
    # If full dataset, 800k rows with LightGBM histograms takes ~30-45s
    # We use 300,000 recent rows or full for peak accuracy
    if len(X_train) > 250000:
        print("Using the most recent 250,000 training records for rapid, high-fidelity fitting...")
        train_sample = train_data.sort_values("Date").tail(250000)
        X_train_fit = train_sample[FEATURE_COLUMNS]
        y_train_fit = train_sample[TARGET_COLUMN]
    else:
        X_train_fit = X_train
        y_train_fit = y_train

    # 4. Build Pipeline
    print("Building scikit-learn preprocessing & LightGBM pipeline...")
    preprocessor = build_preprocessor()

    lgb_regressor = lgb.LGBMRegressor(
        n_estimators=600,
        learning_rate=0.06,
        num_leaves=63,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )

    model_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", lgb_regressor)
    ])

    # 5. Fit model
    print("Fitting LightGBM pipeline...")
    model_pipeline.fit(X_train_fit, y_train_fit)

    # 6. Evaluate on validation set
    print("Evaluating on the out-of-time validation set...")
    val_preds = np.maximum(0, model_pipeline.predict(X_valid))
    val_metrics = calculate_metrics(y_valid, val_preds)
    print(f"Validation Metrics: {val_metrics}")

    # 7. Extract Top Feature Importances
    try:
        fitted_prep = model_pipeline.named_steps["preprocessor"]
        fitted_reg = model_pipeline.named_steps["regressor"]
        feature_names = fitted_prep.get_feature_names_out()
        importances = fitted_reg.feature_importances_
        feat_imp = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:30]
        feature_importance_dict = {name.replace("categorical__", "").replace("numeric__", ""): float(score) for name, score in feat_imp}
    except Exception as e:
        print(f"Warning extracting feature names: {e}")
        feature_importance_dict = {}

    # 8. Save Model and Metadata
    models_dir = os.path.join(current_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    model_save_path = os.path.join(models_dir, "lightgbm_model.joblib")
    print(f"Serializing fitted pipeline to: {model_save_path}")
    joblib.dump(model_pipeline, model_save_path, compress=3)

    # Metadata matching project benchmark results
    metadata = {
        "best_model": "LightGBM",
        "validation_metrics": val_metrics,
        "feature_importances": feature_importance_dict,
        "training_records": int(len(train_df)),
        "unique_stores": int(train_df["Store"].nunique()),
        "date_range": {
            "start": str(train_df["Date"].min().date()),
            "end": str(train_df["Date"].max().date())
        },
        "all_model_benchmarks": [
            {
                "Model": "LightGBM",
                "MAE": 782.961,
                "RMSE": 1100.433,
                "RMSPE (%)": 18.282,
                "Ranking": 1,
                "Status": "Best Model"
            },
            {
                "Model": "Tuned XGBoost",
                "MAE": 867.033,
                "RMSE": 1183.891,
                "RMSPE (%)": 21.122,
                "Ranking": 2,
                "Status": "Runner Up"
            },
            {
                "Model": "XGBoost (Default)",
                "MAE": 1147.503,
                "RMSE": 1487.476,
                "RMSPE (%)": 28.323,
                "Ranking": 3,
                "Status": "Baseline Tree"
            },
            {
                "Model": "Random Forest",
                "MAE": 1539.585,
                "RMSE": 2044.817,
                "RMSPE (%)": 38.541,
                "Ranking": 4,
                "Status": "Ensemble"
            },
            {
                "Model": "Median Baseline",
                "MAE": 2204.307,
                "RMSE": 3115.111,
                "RMSPE (%)": 51.291,
                "Ranking": 5,
                "Status": "Naive Baseline"
            }
        ]
    }

    meta_save_path = os.path.join(models_dir, "model_metadata.json")
    with open(meta_save_path, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Saved benchmark metadata to: {meta_save_path}")

    # 9. Compute and cache summary aggregations for instant dashboard charts
    print("Computing aggregated summary tables for instant dashboard performance...")
    data_dir = os.path.join(current_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # Monthly trends
    train_df["YearMonth"] = train_df["Date"].dt.to_period("M").astype(str)
    monthly_sales = train_df.groupby("YearMonth")["Sales"].agg(["sum", "mean"]).reset_index()
    monthly_sales.columns = ["YearMonth", "TotalSales", "AvgSales"]
    monthly_sales.to_csv(os.path.join(data_dir, "monthly_sales.csv"), index=False)

    # Weekday sales
    weekday_names = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    weekday_sales = train_df.groupby("DayOfWeek")["Sales"].agg(["mean", "count"]).reset_index()
    weekday_sales["DayName"] = weekday_sales["DayOfWeek"].map(weekday_names)
    weekday_sales.to_csv(os.path.join(data_dir, "weekday_sales.csv"), index=False)

    # Promo vs Non-Promo
    promo_sales = train_df.groupby("Promo")["Sales"].agg(["mean", "sum", "count"]).reset_index()
    promo_sales.to_csv(os.path.join(data_dir, "promo_sales.csv"), index=False)

    # Store Type Sales
    merged_summary = train_df.merge(store_df, on="Store", how="left")
    storetype_sales = merged_summary.groupby("StoreType")["Sales"].agg(["mean", "sum", "count"]).reset_index()
    storetype_sales.to_csv(os.path.join(data_dir, "storetype_sales.csv"), index=False)

    # Store KPI lookup
    store_kpi = train_df[train_df["Open"] == 1].groupby("Store")["Sales"].agg(["mean", "max", "min"]).reset_index()
    store_kpi.columns = ["Store", "AvgSales", "MaxSales", "MinSales"]
    store_kpi = store_kpi.merge(store_df, on="Store", how="left")
    store_kpi.to_csv(os.path.join(data_dir, "store_kpi.csv"), index=False)

    print("=" * 60)
    print("Model training & artifact preparation complete!")
    print("=" * 60)


if __name__ == "__main__":
    train_and_save()

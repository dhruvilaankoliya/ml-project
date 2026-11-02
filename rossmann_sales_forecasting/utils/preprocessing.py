import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error

CATEGORICAL_FEATURES = [
    "Store", "DayOfWeek", "StateHoliday", "StoreType", "Assortment", "PromoInterval"
]

NUMERIC_FEATURES = [
    "Promo", "SchoolHoliday", "CompetitionDistance",
    "CompetitionOpenSinceMonth", "CompetitionOpenSinceYear",
    "Promo2", "Promo2SinceWeek", "Promo2SinceYear",
    "Year", "Month", "Day", "WeekOfYear", "IsWeekend"
]

FEATURE_COLUMNS = CATEGORICAL_FEATURES + NUMERIC_FEATURES
TARGET_COLUMN = "Sales"


def build_preprocessor():
    """
    Constructs the shared scikit-learn preprocessing pipeline matching
    the exact specification from the project notebook:
    - Categorical: most_frequent imputer + OneHotEncoder(handle_unknown='ignore')
    - Numeric: median imputer
    """
    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ("numeric", numeric_pipeline, NUMERIC_FEATURES)
    ])

    return preprocessor


def extract_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts time-based features consistent with notebook Step 4:
    Year, Month, Day, WeekOfYear, IsWeekend, DayOfWeek.
    """
    data = df.copy()
    if "Date" in data.columns:
        if not pd.api.types.is_datetime64_any_dtype(data["Date"]):
            data["Date"] = pd.to_datetime(data["Date"])
        data["Year"] = data["Date"].dt.year
        data["Month"] = data["Date"].dt.month
        data["Day"] = data["Date"].dt.day
        data["WeekOfYear"] = data["Date"].dt.isocalendar().week.astype(int)
        data["IsWeekend"] = data["Date"].dt.dayofweek.isin([5, 6]).astype(int)
        if "DayOfWeek" not in data.columns:
            data["DayOfWeek"] = data["Date"].dt.dayofweek + 1

    if "StateHoliday" in data.columns:
        data["StateHoliday"] = data["StateHoliday"].astype(str).replace({"0.0": "0"})

    return data


def calculate_metrics(y_true, y_pred) -> dict:
    """
    Calculates MAE, RMSE, and RMSPE (%) identical to notebook calculation:
    RMSPE is calculated only on non-zero actual sales.
    """
    actual = np.asarray(y_true, dtype=float)
    predicted = np.asarray(y_pred, dtype=float)

    mae = float(mean_absolute_error(actual, predicted))
    rmse = float(np.sqrt(mean_squared_error(actual, predicted)))

    nonzero = actual > 0
    if np.sum(nonzero) > 0:
        rmspe = float(np.sqrt(np.mean(((actual[nonzero] - predicted[nonzero]) / actual[nonzero]) ** 2)) * 100)
    else:
        rmspe = 0.0

    return {
        "MAE": round(mae, 3),
        "RMSE": round(rmse, 3),
        "RMSPE (%)": round(rmspe, 3)
    }


def prepare_prediction_dataframe(store_metadata: dict, date_val, promo: int,
                                 school_holiday: int, state_holiday: str) -> pd.DataFrame:
    """
    Constructs a 1-row DataFrame matching the 19 feature columns for model inference.
    """
    ts = pd.to_datetime(date_val)
    day_of_week = ts.dayofweek + 1
    year = ts.year
    month = ts.month
    day = ts.day
    week_of_year = int(ts.isocalendar().week)
    is_weekend = int(ts.dayofweek in [5, 6])

    row = {
        "Store": int(store_metadata.get("Store", 1)),
        "DayOfWeek": int(day_of_week),
        "StateHoliday": str(state_holiday),
        "StoreType": str(store_metadata.get("StoreType", "a")),
        "Assortment": str(store_metadata.get("Assortment", "a")),
        "PromoInterval": str(store_metadata.get("PromoInterval", "") or ""),
        "Promo": int(promo),
        "SchoolHoliday": int(school_holiday),
        "CompetitionDistance": float(store_metadata.get("CompetitionDistance") or 1000.0),
        "CompetitionOpenSinceMonth": float(store_metadata.get("CompetitionOpenSinceMonth") or 1.0),
        "CompetitionOpenSinceYear": float(store_metadata.get("CompetitionOpenSinceYear") or 2010.0),
        "Promo2": int(store_metadata.get("Promo2", 0)),
        "Promo2SinceWeek": float(store_metadata.get("Promo2SinceWeek") or 0.0),
        "Promo2SinceYear": float(store_metadata.get("Promo2SinceYear") or 0.0),
        "Year": int(year),
        "Month": int(month),
        "Day": int(day),
        "WeekOfYear": int(week_of_year),
        "IsWeekend": int(is_weekend)
    }

    df = pd.DataFrame([row])
    # Ensure categorical string types
    for col in CATEGORICAL_FEATURES:
        df[col] = df[col].astype(str)
    return df[FEATURE_COLUMNS]

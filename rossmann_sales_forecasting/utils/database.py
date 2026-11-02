import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "predictions.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_id INTEGER NOT NULL,
                prediction_date TEXT NOT NULL,
                predicted_sales REAL NOT NULL,
                selected_model TEXT NOT NULL,
                store_type TEXT,
                assortment TEXT,
                promo INTEGER,
                school_holiday INTEGER,
                state_holiday TEXT,
                created_at TEXT NOT NULL
            )
        """)
    conn.close()


def insert_prediction(store_id: int, prediction_date: str, predicted_sales: float,
                      selected_model: str, store_type: str = "", assortment: str = "",
                      promo: int = 0, school_holiday: int = 0, state_holiday: str = "0"):
    init_db()
    conn = get_connection()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with conn:
        cursor = conn.execute("""
            INSERT INTO prediction_history (
                store_id, prediction_date, predicted_sales, selected_model,
                store_type, assortment, promo, school_holiday, state_holiday, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            store_id, str(prediction_date), float(predicted_sales), str(selected_model),
            str(store_type), str(assortment), int(promo), int(school_holiday), str(state_holiday), now_str
        ))
        inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id


def get_all_predictions(store_filter=None, search_query=None) -> pd.DataFrame:
    init_db()
    conn = get_connection()
    query = "SELECT * FROM prediction_history WHERE 1=1"
    params = []

    if store_filter is not None and str(store_filter).strip() != "":
        try:
            query += " AND store_id = ?"
            params.append(int(store_filter))
        except ValueError:
            pass

    if search_query:
        query += " AND (CAST(store_id AS TEXT) LIKE ? OR prediction_date LIKE ? OR selected_model LIKE ?)"
        q = f"%{search_query}%"
        params.extend([q, q, q])

    query += " ORDER BY id DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def delete_prediction(prediction_id: int):
    init_db()
    conn = get_connection()
    with conn:
        conn.execute("DELETE FROM prediction_history WHERE id = ?", (int(prediction_id),))
    conn.close()


def clear_all_predictions():
    init_db()
    conn = get_connection()
    with conn:
        conn.execute("DELETE FROM prediction_history")
    conn.close()

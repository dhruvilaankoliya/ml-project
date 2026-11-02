import streamlit as st
import os
import sys
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
if project_dir not in sys.path:
    sys.path.append(project_dir)

from utils.ui import apply_custom_css, render_page_header
from utils.database import get_all_predictions, delete_prediction, clear_all_predictions

st.set_page_config(page_title="Prediction History - Rossmann AI", page_icon="📜", layout="wide")
apply_custom_css()

render_page_header(
    title="Prediction Audit & Historical Log",
    subtitle="Persistent SQLite Database of Live Forecasts Generated Across Sessions",
    badge="SQLite Managed"
)

# Search & Filter Controls
fc1, fc2, fc3 = st.columns([1, 1, 1])

with fc1:
    search_txt = st.text_input("🔎 Search (Store, Date, or Model):", value="")
with fc2:
    store_filter_val = st.text_input("Filter by Exact Store ID:", value="")
with fc3:
    st.write("") # Spacer
    st.write("")
    btn_refresh = st.button("🔄 Refresh History", use_container_width=True)

# Query SQLite records
df_history = get_all_predictions(
    store_filter=store_filter_val if store_filter_val.strip() else None,
    search_query=search_txt if search_txt.strip() else None
)

# Display Summary KPIs
st.markdown("### 📊 Audit Summary")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Total Predictions Logged", len(df_history))
with k2:
    avg_pred = df_history["predicted_sales"].mean() if not df_history.empty else 0.0
    st.metric("Average Forecast", f"₹{avg_pred:,.2f}")
with k3:
    max_pred = df_history["predicted_sales"].max() if not df_history.empty else 0.0
    st.metric("Peak Forecast", f"₹{max_pred:,.2f}")
with k4:
    unique_stores = df_history["store_id"].nunique() if not df_history.empty else 0
    st.metric("Unique Stores Queried", unique_stores)

st.markdown("<br>", unsafe_allow_html=True)

# Main Table Display
if not df_history.empty:
    st.markdown("### 📋 Prediction History Records")
    
    # Display formatted dataframe
    display_df = df_history[[
        "id", "store_id", "prediction_date", "predicted_sales", 
        "selected_model", "promo", "school_holiday", "created_at"
    ]].copy()
    display_df.columns = [
        "Prediction ID", "Store ID", "Target Date", "Predicted Sales (₹)", 
        "Model", "Promo", "School Holiday", "Generated At"
    ]
    display_df["Predicted Sales (₹)"] = display_df["Predicted Sales (₹)"].apply(lambda x: f"₹{x:,.2f}")
    display_df["Promo"] = display_df["Promo"].map({1: "Yes (Discount)", 0: "No"})
    display_df["School Holiday"] = display_df["School Holiday"].map({1: "Yes", 0: "No"})

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Actions: Download and Delete
    ac1, ac2 = st.columns([1, 1])
    
    with ac1:
        csv_history = df_history.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Full History as CSV",
            data=csv_history,
            file_name="rossmann_prediction_history.csv",
            mime="text/csv",
            use_container_width=True
        )

    with ac2:
        with st.expander("🗑️ Delete Records"):
            del_id = st.number_input("Enter Prediction ID to delete:", min_value=1, step=1)
            confirm_del = st.checkbox("Confirm deletion of this specific audit record?")
            if st.button("Delete Single Record", type="secondary"):
                if confirm_del:
                    delete_prediction(del_id)
                    st.success(f"Record #{del_id} successfully deleted.")
                    st.rerun()
                else:
                    st.error("Please tick the confirmation checkbox first.")
            
            st.markdown("---")
            confirm_all = st.checkbox("⚠️ Check to confirm clearing ALL history permanently")
            if st.button("Clear Entire Audit Log", type="primary"):
                if confirm_all:
                    clear_all_predictions()
                    st.success("All prediction records have been wiped.")
                    st.rerun()
                else:
                    st.error("Confirmation required to wipe all history.")

else:
    st.info("No prediction records found matching your filters. Make a prediction on the **Sales Prediction** page to start populating your SQLite audit log!")

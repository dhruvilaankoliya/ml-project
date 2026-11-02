import streamlit as st
import os
import sys
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
if project_dir not in sys.path:
    sys.path.append(project_dir)

from utils.ui import apply_custom_css, render_page_header
from utils.prediction import load_stores_df

st.set_page_config(page_title="Dataset Explorer - Rossmann AI", page_icon="📁", layout="wide")
apply_custom_css()

render_page_header(
    title="Interactive Dataset Explorer",
    subtitle="Inspect Raw Training and Store Metadata, Null Distributions, Schemas & Filter Records",
    badge="Data Inspection"
)

# Tab selection for datasets
tab_train, tab_store = st.tabs(["📊 Training Dataset (`train.csv`)", "🏬 Store Metadata (`store.csv`)"])

# TAB 1: Training Dataset
with tab_train:
    st.markdown("### 📈 Rossmann Sales Transactions (`train.csv`)")
    
    # Path to train.csv in parent or local
    train_path = os.path.join(os.path.dirname(project_dir), "train.csv")
    if not os.path.exists(train_path):
        train_path = os.path.join(project_dir, "data", "train.csv")

    if os.path.exists(train_path):
        c_rows, c_search = st.columns([1, 2])
        with c_rows:
            sample_size = st.slider("Select Sample Size to Display:", min_value=100, max_value=5000, value=500, step=100)
        with c_search:
            search_store = st.text_input("Filter by Store ID (Optional):", value="")

        # Efficient chunk reading for high performance
        df_train_sample = pd.read_csv(train_path, nrows=10000, low_memory=False)

        if search_store.strip():
            try:
                s_id = int(search_store.strip())
                df_train_sample = df_train_sample[df_train_sample["Store"] == s_id]
            except ValueError:
                pass

        df_display = df_train_sample.head(sample_size)

        # Multi-select columns
        all_train_cols = list(df_train_sample.columns)
        selected_train_cols = st.multiselect("Visible Columns:", options=all_train_cols, default=all_train_cols)

        st.dataframe(df_display[selected_train_cols], use_container_width=True)

        # Meta summary
        st.markdown("#### 🔬 Schema & Missing Values Analysis")
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            schema_df = pd.DataFrame({
                "Column": df_train_sample.columns,
                "Data Type": [str(t) for t in df_train_sample.dtypes],
                "Null Count (in sample)": df_train_sample.isnull().sum().values,
                "Null %": (df_train_sample.isnull().sum().values / len(df_train_sample) * 100).round(2)
            })
            st.dataframe(schema_df, use_container_width=True, hide_index=True)

        with col_s2:
            st.write("""
            **Key Field Definitions:**
            - **Store:** Unique store identifier (1 to 1,115).
            - **DayOfWeek:** 1 = Monday, 7 = Sunday.
            - **Sales:** Daily turnover in Euros (Target Variable).
            - **Customers:** Number of patrons on that day (excluded at prediction time).
            - **Open:** 0 = Closed (Sunday/Holiday), 1 = Open.
            - **Promo:** Indicates whether a store is running a promotion on that day.
            - **StateHoliday:** a = Public, b = Easter, c = Christmas, 0 = None.
            - **SchoolHoliday:** Indicates if public school was closed.
            """)

        # Download sample CSV
        csv_train_dl = df_display[selected_train_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Training Sample as CSV",
            data=csv_train_dl,
            file_name="rossmann_train_sample.csv",
            mime="text/csv"
        )
    else:
        st.error(f"Training dataset not located at {train_path}.")

# TAB 2: Store Metadata
with tab_store:
    st.markdown("### 🏬 Rossmann Store Profiles (`store.csv`)")
    stores_full = load_stores_df()

    s_c1, s_c2 = st.columns([1, 2])
    with s_c1:
        type_choice = st.multiselect("Filter by Store Type:", options=["a", "b", "c", "d"], default=["a", "b", "c", "d"])
    with s_c2:
        search_store_id = st.text_input("Search Store ID:", value="")

    filtered_stores = stores_full[stores_full["StoreType"].isin(type_choice)]
    if search_store_id.strip():
        try:
            filtered_stores = filtered_stores[filtered_stores["Store"] == int(search_store_id.strip())]
        except ValueError:
            pass

    store_cols = list(stores_full.columns)
    selected_store_cols = st.multiselect("Visible Store Attributes:", options=store_cols, default=store_cols)

    st.dataframe(filtered_stores[selected_store_cols], use_container_width=True)

    st.markdown("#### 🔬 Store Attributes & Missing Values Profile")
    sm_c1, sm_c2 = st.columns(2)

    with sm_c1:
        store_nulls = pd.DataFrame({
            "Attribute": stores_full.columns,
            "Data Type": [str(t) for t in stores_full.dtypes],
            "Missing Count": stores_full.isnull().sum().values,
            "Missing %": (stores_full.isnull().sum().values / len(stores_full) * 100).round(2)
        })
        st.dataframe(store_nulls, use_container_width=True, hide_index=True)

    with sm_c2:
        st.write("""
        **Missing Value Insights:**
        - **CompetitionDistance:** Only 3 stores lack distance metrics (median imputation applied).
        - **CompetitionOpenSince:** ~31.7% missing because competition opened prior to tracking or does not exist.
        - **Promo2Since / PromoInterval:** ~48.8% missing because `Promo2 = 0` (store does not participate in continuous promotions). *These null values are structurally meaningful and safely handled.*
        """)

    csv_store_dl = filtered_stores[selected_store_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Store Data as CSV",
        data=csv_store_dl,
        file_name="rossmann_store_metadata.csv",
        mime="text/csv"
    )

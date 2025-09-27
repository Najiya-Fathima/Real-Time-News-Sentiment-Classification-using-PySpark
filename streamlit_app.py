# streamlit_app.py (or app.py) - CORRECTED VERSION

import streamlit as st
import pandas as pd
import os
import time
import pyarrow

# --- Page Configuration ---
st.set_page_config(
    page_title="Live News Sentiment Analysis",
    page_icon="📊",
    layout="wide"
)

# --- App Title ---
st.title("📊 Live News Sentiment Analysis Dashboard")

# --- Directory Path ---
RESULTS_DIR = 'results_parquet'

# --- Function to read data ---
@st.cache_data(ttl=5)
def load_data():
    """Loads all valid parquet files from the results directory into a DataFrame."""
    if not os.path.exists(RESULTS_DIR):
        return pd.DataFrame()

    files = [os.path.join(RESULTS_DIR, f) for f in os.listdir(RESULTS_DIR) if f.endswith('.parquet')]
    
    if not files:
        return pd.DataFrame()

    valid_dfs = []
    for f in files:
        try:
            if os.path.getsize(f) > 0:
                df_part = pd.read_parquet(f)
                valid_dfs.append(df_part)
        except pyarrow.lib.ArrowInvalid:
            pass 

    if not valid_dfs:
        return pd.DataFrame()
        
    df = pd.concat(valid_dfs, ignore_index=True)
    df = df.iloc[::-1].reset_index(drop=True)
    return df

# --- Main App Logic ---
placeholder = st.empty()
df = load_data()

with placeholder.container():
    if not df.empty:
        # --- Metrics ---
        total_headlines = len(df)
        
        # --- THIS IS THE FIX ---
        # Use 'pos' and 'neg' to match the data from Spark NLP
        positive_count = df[df['sentiment'] == 'pos'].shape[0]
        negative_count = df[df['sentiment'] == 'neg'].shape[0]
        neutral_count = df[df['sentiment'] == 'neutral'].shape[0]

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric(label="Total Headlines Processed 📰", value=total_headlines)
        kpi2.metric(label="Positive Headlines ✅", value=positive_count)
        kpi3.metric(label="Negative Headlines ❌", value=negative_count)
        kpi4.metric(label="Neutral Headlines ➖", value=neutral_count)

        # --- Visualization ---
        st.subheader("Sentiment Distribution")
        sentiment_counts = df['sentiment'].value_counts()
        st.bar_chart(sentiment_counts)
        
        # --- Raw Data View ---
        st.subheader("All Processed Headlines")
        st.dataframe(df[['sentiment', 'headline']])
    else:
        st.info("Waiting for data from the data_producer.py...")

st.button("Refresh Data")
time.sleep(10)
st.rerun()
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json
import os

from data.processor import process_flight_data, apply_filters
from utils.download import get_csv_download_link
from insights.analyzer import summarize_text, prepare_summary_text

if "df_raw" not in st.session_state:
    st.session_state.df_raw = pd.DataFrame()

# ------------------- Config -------------------
API_KEY = "647dbc4d1ce8b2b57e5c1a1f8032eba7"
API_URL = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&limit=100"
CACHE_FILE = "flights.json"

# ------------------- Fetch + Cache -------------------
def fetch_flight_data():
    try:
        st.info("Fetching data from AviationStack API...")
        response = requests.get(API_URL)
        data = response.json()

      

        if "data" in data:
            with open(CACHE_FILE, "w") as f:
                json.dump(data, f)
            st.success("Live data fetched and cached successfully.")
            return data
        else:
            st.warning("No data returned from API.")
            return None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

    


def load_cached_data():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    else:
        st.warning("No cached data found.")
        return None

# ------------------- Streamlit UI -------------------
st.set_page_config(page_title="Airline Demand Dashboard", layout="centered")
st.title("✈️ Airline Booking Market Demand Dashboard")

with st.sidebar:
    st.header("🔧 Controls")
    fetch_button = st.button("Fetch Live Data (1 API call)")
    load_button = st.button("Load Cached Data")

# Initialize dataframe
df = pd.DataFrame()

if fetch_button:
    data = fetch_flight_data()
    if data:
        st.session_state.df_raw = process_flight_data(data)

elif load_button:
    data = load_cached_data()
    if data:
        st.session_state.df_raw = process_flight_data(data)

df = st.session_state.df_raw



# ------------------- Display -------------------
if not df.empty:
    st.sidebar.subheader("📌 Filters for Top 10 Routes")
    top_airlines = sorted(df['airline'].dropna().unique())
    top_selected_airlines = st.sidebar.multiselect("Airlines (Top 10)", top_airlines, key="top_routes_airlines")

    top_routes_list = sorted([f"{f} → {t}" for f, t in df[['from', 'to']].dropna().drop_duplicates().values])
    top_selected_routes = st.sidebar.multiselect("Routes (Top 10)", top_routes_list, key="top_routes_list")

    df_top = df.copy()
    df_top = apply_filters(df_top, top_selected_airlines, top_selected_routes)

    st.subheader("📊 Top 10 Popular Routes")
    top_routes = df_top.groupby(['from', 'to']).size().reset_index(name='count')
    top_routes = top_routes.sort_values('count', ascending=False).head(10)
    st.dataframe(top_routes)

    fig1 = px.bar(top_routes, x='count', y='to', color='from', orientation='h',
                  title="Most Frequent Routes")
    st.plotly_chart(fig1)

    # ------------------- Filters for Detailed Table -------------------
    st.sidebar.subheader("📌 Filters for Detailed Table & Insights")

    detail_airlines = sorted(df['airline'].dropna().unique())
    selected_airlines = st.sidebar.multiselect("Airlines (Details)", detail_airlines, key="detail_airlines")

    detail_routes = sorted([f"{f} → {t}" for f, t in df[['from', 'to']].dropna().drop_duplicates().values])
    selected_routes = st.sidebar.multiselect("Routes (Details)", detail_routes, key="detail_routes")

    df_detail = df.copy()
    df_detail = apply_filters(df_detail, selected_airlines, selected_routes)

    # ------------------- Detailed Table -------------------
    st.subheader("📋 Detailed Flight Data")

    display_cols = [
        'flight_date',
        'flight_status',
        'airline',
        'flight_number',
        'from', 'from_iata',
        'to', 'to_iata',
        'departure_time',
        'arrival_time'
    ]

    st.dataframe(df_detail[display_cols].sort_values(by='departure_time'))

    st.subheader("📈 Flight Volume Over Time")
    flights_time = df_detail.groupby(df_detail['departure_time'].dt.date).size().reset_index(name='flights')
    st.line_chart(flights_time.set_index('departure_time'))

    # ------------------- Download Button -------------------
    st.subheader("📥 Download Filtered Data")
    csv_data, filename = get_csv_download_link(df_detail)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name=filename,
        mime='text/csv'
    )

    # ------------------- AI Insight Section -------------------
    st.subheader("🧠 AI-Generated Insights")
    with st.spinner("Analyzing data with AI..."):
        summary_text = prepare_summary_text(df_detail)
        ai_summary = summarize_text(summary_text)
        st.success("Insights generated!")
        st.markdown(f"**Summary:** {ai_summary}")

else:
    st.info("Use the sidebar to fetch or load data.")

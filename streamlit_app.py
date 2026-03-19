import streamlit as st
import requests
import pandas as pd
import urllib.parse
import time

# --- Config ---
API_KEY = st.secrets["API_KEY"]
EMAIL = st.secrets["EMAIL"]
BASE_URL = 'https://developer.nlr.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv?'
YEAR = '2024'

# --- UI ---
st.title("NREL Solar Data Downloader")
st.markdown("Enter a location to download hourly relative humidity and air temperature data.")

lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=34.058649, format="%.6f")
lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=-106.892611, format="%.6f")

if st.button("Fetch Data"):
    wkt = f'POINT({lon} {lat})'

    input_data = {
        'attributes': 'relative_humidity,air_temperature',
        'interval': '60',
        'wkt': wkt,
        'names': [YEAR],
        'location_ids': 'wkt',
        'api_key': API_KEY,
        'email': EMAIL,
    }

    with st.spinner("Fetching data from NREL..."):
        try:
            url = BASE_URL + urllib.parse.urlencode(input_data, True)
            data = pd.read_csv(url)

            st.success("Data fetched successfully!")
            st.dataframe(data.head(20))

            csv_bytes = data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv_bytes,
                file_name=f"NREL_{lat}_{lon}.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Something went wrong: {e}")

import streamlit as st
from utils.io import load_crimes, load_geojson, load_socio
from charts.charts import (chart_crime_time,)

df = load_crimes()
socio = load_socio()
chi_map = load_geojson()

st.title("Interactive Exploratory View")
st.write("Use the interactive charts below to explore the data at your own pace.")

st.subheader("Chicago Citywide Crime Trends")
st.altair_chart(chart_crime_time(df), use_container_width = True)

st.markdown("**Guided prompts:**")
st.write("placeholder")
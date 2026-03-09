import streamlit as st
from utils.io import load_crimes, load_geojson, load_socio
from charts.charts import (
    chart_crime_time,
)

df = load_crimes()
socio = load_socio()
chi_map = load_geojson()

st.title("Crime and Socioeconomic Factors in Chicago: A Data Story")
st.markdown("**Central Question**:")

st.header("1) How has crime in Chicago changed over time?")
st.write("We start with a broad view. This chart shows the total reported crimes in Chicago from 2001 - Present."
)
st.altair_chart(chart_crime_time(df), use_container_width = True)
st.caption("Takeaway: Reported crimes in Chicago generally declined steadily from the early 2000s to the mid-2010s, followed by a relatively stable period and then fluctuations in recent years. The sharp drop in the final year likely reflects incomplete data for the current year rather than an actual decline, which is important to consider when interpreting the trend.")

st.divider()

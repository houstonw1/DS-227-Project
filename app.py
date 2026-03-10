import streamlit as st
from PIL import Image

st.set_page_config(page_title = "Crime and Socioeconomic Factors in Chicago", layout = "wide")

st.title("Crime and Socioeconomic Factors in Chicago")
st.write(Image.open('images/crime_chloropleth.png'))
st.write("To explore this visual data story, please navigate it through the pages in the sidebar:\n"
"- **Central Narrative**: Crime in Chicago is not random — it is deeply concentrated in neighborhoods shaped by decades of economic inequality, and this data story examines where, how, and why.\n"
"- **Story**: Follow the narrative through guided visualizations.\n"
"- **Exploration**: For a closer reader-driven exploration of the data we provide more interactive designs.\n"
"- **Methodology**: We lay down some key details about our data and limitations to our analysis.\n"
)
st.info("Datasets: `Crimes.csv`, `Chicago_Socioeco_2008_2012.csv`, and `chicago-ward-boundaries.geojson`")
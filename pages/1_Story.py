import streamlit as st
from utils.io import load_agg_yearly, load_agg_community_poverty, load_agg_income_crime
from charts.charts import (
    chart_crime_time,
    chart_arrests_reports,
    chart_income_crime,
)

df = load_agg_yearly()
df_community_poverty = load_agg_community_poverty()
df_income_crime = load_agg_income_crime()

st.title("Crime and Socioeconomic Factors in Chicago: A Data Story")
st.markdown("**Central Question**: How do crime patterns across Chicago relate to socioeconomic conditions in specific neighborhoods?")

st.write("""
In this project, we aim to examine whether certain neighborhoods experience different trends in crime rates,
how these trends have evolved from 2001 to the present, and whether possible shifts in crime coincide with
income, unemployment, or population density. The goal is to understand Chicago's long-run structural patterns
in public safety.
""")

st.write("""
Our primary dataset is **Crimes - 2001 to Present**, provided by the Chicago Police Department through
the City of Chicago Data Portal. The dataset includes reported incidents of crime in Chicago from 2001
to the present (excluding the most recent seven days). This dataset is suitable for the analysis because
it contains spatial identifiers, consistent reporting over more than two decades, and detailed crime
classifications that allow for neighborhood-level comparison.

Additional datasets used in the project include unemployment, population characteristics, and income data, which can be retrieved from the American Community Survey and merged using geographic identifiers such as community area.
""")

st.divider()

st.header("1. How has crime in Chicago changed over time?")
st.write("We start with a broad view. This chart shows the total reported crimes in Chicago from 2001 - Present.")
st.altair_chart(chart_crime_time(df), use_container_width=True)
st.caption("Takeaway: Reported crimes in Chicago generally declined steadily from the early 2000s to the mid-2010s, followed by a relatively stable period and then fluctuations in recent years. The sharp drop in the final year likely reflects incomplete data for the current year rather than an actual decline, which is important to consider when interpreting the trend.")

st.divider()

st.header("2. How does community area's percentage of households below poverty affect the amount of reported crimes vs actual arrest?")
st.write("This chart directly connects crime to socioeconomic data. We examine whether the community areas with the highest crime reports have the highest arrest rates and all in relation to percentage of households below poverty.")
st.altair_chart(chart_arrests_reports(df_community_poverty), use_container_width=True)
st.caption("Takeaway: Darker blue bars indicate higher poverty and are more common among the highest arrest totals rather than report totals. Areas that see more significant poverty, typically have higher arrest totals vs report totals.")

st.divider()

st.header("3. How does the most common type of crime change across the highest and lowest income per capita community areas?")
st.write("Comparing the 15 highest and lowest income community areas reveals differences in both crime volume and dominant crime type.")
st.altair_chart(chart_income_crime(df_income_crime), use_container_width=True)
st.caption("Takeaway: Low-income areas have higher crime totals and dominant crime types of Narcotics and Battery. High-income areas are consistently dominated by theft. This implies an inequality that socioeconomic conditions shape not just how much crime occurs, but what kind of crime communities are exposed to.")

st.divider()

st.markdown("""
Next, we dive deep to explore the central question with an array of visualizations. The first
visualizations establish the broader context, showing how total crime has changed over time and
how major crime categories have evolved. These charts reveal long-term shifts in crime levels
and highlight which types of crimes are most common.

Subsequent visualizations focus on geographic pattern to demonstrate that crime is not evenly
distributed across the city. Maps and rankings of community areas show that certain neighborhoods
consistently experience higher crime levels, while others remain relatively lower. Distribution
charts further illustrate that a small number of areas account for a disproportionately large
share of total crime.

The later visualizations incorporate socioeconomic indicators, such as poverty and income levels,
to examine how crime relates to neighborhood conditions. These comparisons suggest that areas with
higher poverty rates and lower income levels often appear among those with higher crime counts and
arrests, while higher-income areas tend to have lower crime totals and different dominant crime
types. Together, the visualizations provide a multi-angle view suggesting that crime patterns in
Chicago are closely connected to underlying socioeconomic inequalities across neighborhoods.
""")

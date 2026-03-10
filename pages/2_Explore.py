import streamlit as st
from utils.io import load_crimes, load_geojson, load_socio
from charts.charts import (
    chart_crime_time,
    chart_crime_type_trends,
    chart_top15_communities,
    chart_crime_distribution,
    chart_arrest_rate_map,
    chart_violent_vs_property,
    chart_interactive_ward_map,
    chart_arrests_reports,
    chart_income_crime,
)

df = load_crimes()
socio = load_socio()
chi_map = load_geojson()

st.title("Interactive Exploratory View")
st.write("Use the interactive charts below to explore the data at your own pace.")

# --- Chart 1 ---
st.subheader("1. Chicago Citywide Crime Trends")
st.altair_chart(chart_crime_time(df), use_container_width=True)
st.markdown("""
We visualize using a line chart because it is the most effective way to visualize how a quantity
changes over time and allows viewers to easily observe long-term trends. The points on the line
also help highlight the exact value for each year and make year-to-year comparisons clearer.
The visualization shows that reported crimes in Chicago generally declined steadily from the early
2000s to the mid-2010s, followed by a relatively stable period and then fluctuations in recent years.
The sharp drop in the final year likely reflects incomplete data for the current year rather than
an actual decline, which is important to consider when interpreting the trend.
""")

# --- Chart 2 ---
st.subheader("2. Crime Type Trends Over Time (Top 5 Categories)")
st.altair_chart(chart_crime_type_trends(df), use_container_width=True)
st.markdown("""
We visualize the top five crime categories using multiple line plots because they allow trends
for each crime type to be compared over time without the lines overlapping and becoming difficult
to interpret. By separating each crime category into its own panel while keeping the same time axis,
viewers can easily observe how different crime types change independently. The visualization shows
that most major crime categories, such as battery, theft, and criminal damage, generally declined
over the past two decades, reflecting an overall reduction in reported crimes in Chicago. However,
the magnitude and timing of the decline vary across categories, suggesting that different types of
crimes respond differently to social, economic, or policy changes over time.
""")

# --- Chart 3 ---
st.subheader("3. Crime Concentration by Community Area (Top 15)")
st.altair_chart(chart_top15_communities(df), use_container_width=True)
st.markdown("""
We used a horizontal bar chart to compare the total number of crimes across the top 15 community
areas because bar charts are effective for ranking and comparing categorical values. Sorting the
bars in descending order makes it easy to quickly identify which community areas have the highest
concentration of reported crimes. The visualization shows that Community Area 25 has the highest
number of reported crimes, followed by several other areas with similarly high totals, indicating
that crime is unevenly distributed across Chicago. This suggests that certain neighborhoods
experience significantly higher crime levels than others, highlighting areas where public safety
resources and policy attention may be most needed.
""")

# --- Chart 4 ---
st.subheader("4. Distribution of Crime Counts Across Community Areas")
st.altair_chart(chart_crime_distribution(df), use_container_width=True)
st.markdown("""
We used a histogram to visualize how total crime counts are distributed across Chicago's community
areas because histograms are effective for showing the frequency distribution of a continuous
variable. This allows us to see whether crime totals are evenly spread or concentrated in certain
ranges. The chart shows that most community areas fall within the lower to mid ranges of total
crime counts, while only a few areas have extremely high totals. This right-skewed distribution
indicates that crime is concentrated in a small number of community areas rather than being evenly
distributed across the city.
""")

# --- Chart 5 ---
st.subheader("5. Arrest Rate by Chicago Ward")
import streamlit.components.v1 as components
components.html(chart_arrest_rate_map(df, chi_map).to_html(), height=650)
st.markdown("""
We used a choropleth map to visualize arrest rates by Chicago ward because geographic maps are
effective for revealing spatial patterns across locations. By coloring each ward based on its
arrest rate, the visualization makes it easy to identify which parts of the city have relatively
higher or lower arrest rates. The map shows that some central and southern wards have noticeably
higher arrest rates, while other areas display lighter shades, indicating lower rates. This spatial
variation suggests that enforcement outcomes differ across neighborhoods, which may reflect
differences in policing practices, crime patterns, or local conditions.
""")

# --- Chart 6 ---
st.subheader("6. Violent Crime vs. Property Crime by Ward")
st.vega_lite_chart(chart_violent_vs_property(df, chi_map).to_dict(), use_container_width=True)
st.markdown("""
We used side-by-side choropleth maps to compare violent crime and property crime because maps are
well suited for showing spatial patterns, and placing the two maps next to each other makes
geographic differences easier to compare directly. Using the same color scheme across both panels
helps highlight differences in concentration while keeping the comparison visually consistent.
The visualization shows that property crime is much more widespread and concentrated in several
wards, especially in central and some southern parts of Chicago, while violent crime appears lower
in overall volume and more spatially concentrated. This suggests that different types of crime are
not distributed uniformly across the city and that property crime and violent crime may have
distinct neighborhood patterns.
""")

# --- Chart 7 ---
st.subheader("7. Interactive Crime Distribution by Ward and Year")
components.html(chart_interactive_ward_map(df, chi_map).to_html(), height=700)
st.markdown("""
We used an interactive choropleth map with a year slider because it allows viewers to examine how
the spatial distribution of crime changes over time rather than seeing only a single static snapshot.
For the 2001 year alone, the visualization shows that crime is consistently concentrated in certain
wards, especially in parts of central and southern Chicago, while other wards remain relatively
lower across time.
""")

# --- Chart 8 ---
st.subheader("8. Top 15 Community Areas - Poverty in Relation to Crime Report and Arrest Totals")
st.altair_chart(chart_arrests_reports(df, socio), use_container_width = True)
st.markdown("""
    We used side-by-side horizontal bar charts to compare the top community areas by total crimes 
    and by total arrests because this layout makes it easy to see whether the same neighborhoods 
    appear in both rankings. Coloring the bars by percent of households below poverty adds a third 
    variable without overcrowding the figure, allowing the chart to connect crime and arrest patterns 
    with socioeconomic conditions. The visualization shows that some community areas, such as 25, rank 
    highly in both total crimes and total arrests, while others differ between the two measures, 
    suggesting that crime volume and arrest volume do not always move together. The darker blue shading 
    in several high-crime or high-arrest areas also suggests that neighborhoods with higher poverty levels 
    may be more strongly represented among these areas, pointing to a possible relationship between public safety 
    outcomes and structural disadvantage.
""")

# --- Chart 9 ---
st.subheader("9. Top 15 Highest and Lowest Income Areas vs Most Common Crime Type")
st.altair_chart(chart_income_crime(df, socio), use_container_width = True)
st.markdown("""
    We used side-by-side horizontal bar charts to compare the highest-income and lowest-income community 
    areas because this layout makes differences in total crime levels between the two groups easy to 
    see directly. Coloring the bars by each area's most common crime type adds another layer of information 
    without making the chart too crowded, allowing both crime volume and crime composition to be compared 
    at once. The visualization shows that the lowest-income community areas generally have higher total 
    crime counts than the highest-income areas, and their most common crimes are more varied, including 
    battery and narcotics. In contrast, the highest-income community areas are more consistently dominated 
    by theft, suggesting that both the amount and type of crime may differ systematically across neighborhoods 
    with different income levels.
""")
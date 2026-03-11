import streamlit as st
import streamlit.components.v1 as components
from utils.io import (
    load_agg_yearly, load_agg_year_type, load_agg_community,
    load_agg_ward, load_agg_ward_year, load_agg_ward_category,
    load_geojson
)
from charts.charts import (
    chart_crime_time, chart_crime_type_trends, chart_top15_communities,
    chart_crime_distribution, chart_arrest_rate_map,
    chart_violent_vs_property, chart_interactive_ward_map,
)

df_yearly = load_agg_yearly()
df_year_type = load_agg_year_type()
df_community = load_agg_community()
df_ward = load_agg_ward()
df_ward_year = load_agg_ward_year()
df_ward_cat = load_agg_ward_category()
chi_map = load_geojson()

st.title("Interactive Exploratory View")
st.write("Use the interactive charts below to explore the data at your own pace.")

st.subheader("1. Chicago Citywide Crime Trends")
st.altair_chart(chart_crime_time(df_yearly), use_container_width=True)
st.markdown("We visualize using a line chart because it is the most effective way to visualize how a quantity changes over time and allows viewers to easily observe long-term trends. The points on the line also help highlight the exact value for each year and make year-to-year comparisons clearer. The visualization shows that reported crimes in Chicago generally declined steadily from the early 2000s to the mid-2010s, followed by a relatively stable period and then fluctuations in recent years. The sharp drop in the final year likely reflects incomplete data for the current year rather than an actual decline, which is important to consider when interpreting the trend.")

st.subheader("2. Crime Type Trends Over Time (Top 5 Categories)")
st.altair_chart(chart_crime_type_trends(df_year_type), use_container_width=True)
st.markdown("We visualize the top five crime categories using multiple line plots because they allow trends for each crime type to be compared over time without the lines overlapping and becoming difficult to interpret. By separating each crime category into its own panel while keeping the same time axis, viewers can easily observe how different crime types change independently. The visualization shows that most major crime categories, such as battery, theft, and criminal damage, generally declined over the past two decades, reflecting an overall reduction in reported crimes in Chicago. However, the magnitude and timing of the decline vary across categories, suggesting that different types of crimes respond differently to social, economic, or policy changes over time.")

st.subheader("3. Crime Concentration by Community Area (Top 15)")
st.altair_chart(chart_top15_communities(df_community), use_container_width=True)
st.markdown("We used a horizontal bar chart to compare the total number of crimes across the top 15 community areas because bar charts are effective for ranking and comparing categorical values. Sorting the bars in descending order makes it easy to quickly identify which community areas have the highest concentration of reported crimes. The visualization shows that Community Area 25 has the highest number of reported crimes, followed by several other areas with similarly high totals, indicating that crime is unevenly distributed across Chicago. This suggests that certain neighborhoods experience significantly higher crime levels than others, highlighting areas where public safety resources and policy attention may be most needed.")

st.subheader("4. Distribution of Crime Counts Across Community Areas")
st.altair_chart(chart_crime_distribution(df_community), use_container_width=True)
st.markdown("We used a histogram to visualize how total crime counts are distributed across Chicago's community areas because histograms are effective for showing the frequency distribution of a continuous variable. This allows us to see whether crime totals are evenly spread or concentrated in certain ranges. The chart shows that most community areas fall within the lower to mid ranges of total crime counts, while only a few areas have extremely high totals. This right-skewed distribution indicates that crime is concentrated in a small number of community areas rather than being evenly distributed across the city.")

st.subheader("5. Arrest Rate by Chicago Ward")
components.html(chart_arrest_rate_map(df_ward, chi_map).to_html(), height=650)
st.markdown("We used a choropleth map to visualize arrest rates by Chicago ward because geographic maps are effective for revealing spatial patterns across locations. By coloring each ward based on its arrest rate, the visualization makes it easy to identify which parts of the city have relatively higher or lower arrest rates. The map shows that some central and southern wards have noticeably higher arrest rates, while other areas display lighter shades, indicating lower rates. This spatial variation suggests that enforcement outcomes differ across neighborhoods, which may reflect differences in policing practices, crime patterns, or local conditions.")

st.subheader("6. Violent Crime vs. Property Crime by Ward")
st.altair_chart(chart_violent_vs_property(df_ward_cat, chi_map), use_container_width=True)
st.markdown("We used side-by-side choropleth maps to compare violent crime and property crime because maps are well suited for showing spatial patterns, and placing the two maps next to each other makes geographic differences easier to compare directly. Using the same color scheme across both panels helps highlight differences in concentration while keeping the comparison visually consistent. The visualization shows that property crime is much more widespread and concentrated in several wards, especially in central and some southern parts of Chicago, while violent crime appears lower in overall volume and more spatially concentrated. This suggests that different types of crime are not distributed uniformly across the city and that property crime and violent crime may have distinct neighborhood patterns.")

st.subheader("7. Interactive Crime Distribution by Ward and Year")
components.html(chart_interactive_ward_map(df_ward_year, chi_map).to_html(), height=700)
st.markdown("We used an interactive choropleth map with a year slider because it allows viewers to examine how the spatial distribution of crime changes over time rather than seeing only a single static snapshot. For the 2001 year alone, the visualization shows that crime is consistently concentrated in certain wards, especially in parts of central and southern Chicago, while other wards remain relatively lower across time.")

st.divider()
st.subheader("Conclusion")
st.markdown("""
This analysis set out to examine how crime patterns across Chicago relate to socioeconomic
conditions in different neighborhoods. Across nine visualizations, a consistent and troubling
picture emerges.

Chicago's overall crime rate has declined significantly since the early 2000s, yet this
improvement has not been felt equally across the city. Crime remains heavily concentrated in
a small number of community areas, with just a handful of neighborhoods accounting for a
disproportionately large share of total reported incidents. Geographic maps further reveal
that arrest rates, violent crime, and property crime each follow distinct spatial patterns,
clustering in specific wards rather than spreading evenly across the city.

When socioeconomic data is layered onto these patterns, the connection becomes difficult to
ignore. Community areas with higher poverty rates consistently appear among those with the
most crimes and arrests. Low-income neighborhoods are not only exposed to more crime overall,
but also to fundamentally different types of crime — including battery and narcotics — compared
to higher-income areas, where theft dominates.

These findings suggest that crime in Chicago is not random, but deeply shaped by structural
inequality. Addressing long-term public safety challenges in the city will likely require
tackling the underlying socioeconomic conditions that concentrate disadvantage in specific
neighborhoods.
""")


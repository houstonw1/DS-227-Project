import streamlit as st

st.set_page_config(page_title = "Methods", layout = "wide")

st.title("Methods & Limitations")

st.subheader("Methods:")
st.write("""
This project uses the *Crimes - 2001 to Present* dataset from the Chicago Police Department,
accessed through the City of Chicago Data Portal. The dataset contains reported incidents
of crime in Chicago from 2001 to the present.

We first cleaned the data by removing records with missing geographic identifiers and
extracting the year from the reported crime date. Crime incidents were then aggregated
by year and by community area to analyze temporal and spatial patterns.

To explore possible relationships between crime and socioeconomic conditions, we integrated
additional neighborhood-level data including income, unemployment, and population
characteristics from the American Community Survey. These datasets were merged using
geographic identifiers such as Chicago community areas.

The visualizations in this project summarize crime counts over time and across
neighborhoods to identify patterns that may be associated with socioeconomic conditions.
""")

st.subheader("Limitations:")
st.write("""
Several limitations should be considered when interpreting this analysis.

First, the dataset includes only crimes that were reported to the Chicago Police
Department. Reported crime may differ from actual crime levels due to differences
in reporting behavior across neighborhoods.

Second, many visualizations use total crime counts rather than per-capita rates.
Areas with larger populations or higher foot traffic may naturally show higher
crime totals even if the risk to individual residents is not higher.

Third, the most recent year in the dataset may appear artificially low because
the data for the current year is incomplete.

Fourth, the additional dataset with socioeconomic data only had from year 2008-2012 which limits comparison of full scope of crime data we have of 2001-2025,

Finally, this analysis identifies correlations between crime patterns and
socioeconomic conditions but cannot establish causal relationships between
these factors.
""")

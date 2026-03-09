import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title = "Title", layout = "wide")

def chart_crime_time(df: pd.DataFrame) -> alt.Chart:
    df_yearly = (df.groupby("year").size().reset_index(name="total_crimes"))
    return(
        alt.Chart(df_yearly).mark_line(point=True).encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("total_crimes:Q", title="Total Crimes", axis=alt.Axis(format='~s')),
            tooltip=[
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("total_crimes:Q", title="Total Crimes", format=",.0f")
            ]
        ).properties(height=400, title="Total Reported Crimes in Chicago (2001–Present)")
    )

#Checking

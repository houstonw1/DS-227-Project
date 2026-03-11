import streamlit as st
import pandas as pd 
import os
import gdown

@st.cache_data
def load_crimes() -> pd.DataFrame:
    if not os.path.exists("Crimes.csv"):
        gdown.download(
            "https://drive.google.com/uc?id=10BTXAs3nVkwz6206weO0SzT3Jjvxb-0g",
            "Crimes.csv",
            quiet=False
        )
    df = pd.read_csv("Crimes.csv")
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    violent_crimes = [
        "HOMICIDE", "ASSAULT", "BATTERY",
        "CRIMINAL SEXUAL ASSAULT", "ROBBERY"
    ]
    df["crime_category"] = df["primary_type"].apply(
        lambda x: "Violent Crime" if x in violent_crimes else "Property Crime"
    )
    return df
    
@st.cache_data
def load_socio() -> pd.DataFrame:
    socio = pd.read_csv("Chicago_Socioeco_2008_2012.csv")
    socio.columns = socio.columns.str.strip()
    socio = socio.dropna(subset=["Community Area Number"])
    socio["Community Area Number"] = socio["Community Area Number"].astype(int)
    socio = socio.rename(columns={
        "Community Area Number": "community_area",
        "PERCENT HOUSEHOLDS BELOW POVERTY": "pct_below_poverty",
        "PER CAPITA INCOME": "per_capita_income",
        "HARDSHIP INDEX": "hardship_index",
    })
    return socio

@st.cache_data
def load_geojson():
    import json
    with open("chicago-ward-boundaries.geojson") as f:
        return json.load(f)
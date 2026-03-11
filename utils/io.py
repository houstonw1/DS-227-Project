import streamlit as st
import pandas as pd
import json

@st.cache_data
def load_crimes() -> pd.DataFrame:
    # Load from pre-aggregated files instead of raw CSV
    # This is a compatibility shim that returns a minimal df for charts
    # that still need the raw-style interface
    yearly = pd.read_csv("agg_yearly.csv")
    year_type = pd.read_csv("agg_year_type.csv")
    return {"yearly": yearly, "year_type": year_type}

@st.cache_data
def load_agg_yearly() -> pd.DataFrame:
    return pd.read_csv("agg_yearly.csv")

@st.cache_data
def load_agg_year_type() -> pd.DataFrame:
    return pd.read_csv("agg_year_type.csv")

@st.cache_data
def load_agg_community() -> pd.DataFrame:
    return pd.read_csv("agg_community.csv")

@st.cache_data
def load_agg_ward() -> pd.DataFrame:
    return pd.read_csv("agg_ward.csv")

@st.cache_data
def load_agg_ward_year() -> pd.DataFrame:
    df = pd.read_csv("agg_ward_year.csv")
    df["ward"] = df["ward"].astype(int).astype(str)
    df["year"] = df["year"].astype(int)
    return df

@st.cache_data
def load_agg_ward_category() -> pd.DataFrame:
    df = pd.read_csv("agg_ward_category.csv")
    df["ward"] = df["ward"].astype(int).astype(str)
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
    with open("chicago-ward-boundaries.geojson") as f:
        return json.load(f)
        
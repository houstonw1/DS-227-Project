import pandas as pd
import altair as alt
import bokeh.palettes
import copy


def chart_crime_time(df):
    df_yearly = df.groupby("year").size().reset_index(name="total_crimes")
    return alt.Chart(df_yearly).mark_line(point=True).encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("total_crimes:Q", title="Total Crimes", axis=alt.Axis(format='~s')),
        tooltip=[
            alt.Tooltip("year:O", title="Year"),
            alt.Tooltip("total_crimes:Q", title="Total Crimes", format=",.0f")
        ]
    ).properties(height=400, title="Total Reported Crimes in Chicago (2001–Present)")


def chart_crime_type_trends(df):
    top5 = (
        df.groupby("primary_type").size()
        .reset_index(name="total_count")
        .sort_values("total_count", ascending=False)
        ["primary_type"].head(5).tolist()
    )
    df_year_type = (
        df[df["primary_type"].isin(top5)]
        .groupby(["year", "primary_type"]).size()
        .reset_index(name="crime_count")
    )
    return alt.Chart(df_year_type).mark_line(point=True).encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("crime_count:Q", title="Number of Crimes", axis=alt.Axis(format='~s')),
        color=alt.Color("primary_type:N", legend=None),
        tooltip=[
            alt.Tooltip("year:O", title="Year"),
            alt.Tooltip("primary_type:N", title="Crime Type"),
            alt.Tooltip("crime_count:Q", title="Count", format=",.0f")
        ]
    ).properties(
        width=250, height=250,
        title="Trends of Top 5 Crime Categories Over Time"
    ).facet(column=alt.Column("primary_type:N", title="Crime Category"))


def chart_top15_communities(df):
    df_community = (
        df.groupby("community_area").size()
        .reset_index(name="total_crimes")
        .dropna(subset=["community_area"])
    )
    df_community["community_area"] = df_community["community_area"].astype(int)
    df_top15 = df_community.sort_values("total_crimes", ascending=False).head(15)
    return alt.Chart(df_top15).mark_bar().encode(
        x=alt.X("total_crimes:Q", title="Total Crimes", axis=alt.Axis(format='~s')),
        y=alt.Y("community_area:O", sort="-x", title="Community Area"),
        tooltip=[
            alt.Tooltip("community_area:O", title="Community Area"),
            alt.Tooltip("total_crimes:Q", title="Total Crimes", format=",.0f")
        ]
    ).properties(height=400, title="Top 15 Community Areas by Total Reported Crimes (2001–Present)")


def chart_crime_distribution(df):
    df_community = (
        df.groupby("community_area").size()
        .reset_index(name="total_crimes")
        .dropna(subset=["community_area"])
    )
    return alt.Chart(df_community).mark_bar().encode(
        x=alt.X("total_crimes:Q", bin=alt.Bin(maxbins=30), title="Total Crimes per Community Area"),
        y=alt.Y("count():Q", title="Number of Community Areas"),
        tooltip=[alt.Tooltip("count():Q", title="Community Count")]
    ).properties(height=400, title="Distribution of Crime Totals Across Chicago Community Areas")


def chart_arrest_rate_map(df, chi_map):
    alt.data_transformers.disable_max_rows()
    df_ward = (
        df.groupby("ward")
        .agg(total_crimes=("id", "count"), total_arrests=("arrest", "sum"))
        .reset_index()
    )
    df_ward["ward"] = df_ward["ward"].astype(int).astype(str)
    df_ward["arrest_rate"] = df_ward["total_arrests"] / df_ward["total_crimes"]
    ward_lookup = df_ward.set_index("ward").to_dict("index")

    features = copy.deepcopy(chi_map["features"])
    for feature in features:
        ward = str(feature["properties"]["ward"])
        feature["properties"]["arrest_rate"] = round(ward_lookup.get(ward, {}).get("arrest_rate", 0), 4)
        feature["properties"]["total_crimes"] = int(ward_lookup.get(ward, {}).get("total_crimes", 0))

    palette_red = bokeh.palettes.Reds[256][::-1]
    return alt.Chart(
        alt.Data(values=features)
    ).mark_geoshape(
        stroke="white", strokeWidth=0.5
    ).encode(
        color=alt.Color(
            "properties.arrest_rate:Q",
            scale=alt.Scale(range=palette_red),
            legend=alt.Legend(title="Arrest Rate")
        ),
        tooltip=[
            alt.Tooltip("properties.ward:O", title="Ward"),
            alt.Tooltip("properties.total_crimes:Q", title="Total Crimes", format=",.0f"),
            alt.Tooltip("properties.arrest_rate:Q", title="Arrest Rate", format=".2%")
        ]
    ).properties(
        width=600, height=600,
        title="Arrest Rate by Chicago Ward"
    ).project(type="mercator")


def chart_violent_vs_property(df, chi_map):
    alt.data_transformers.disable_max_rows()
    violent_crimes = ["HOMICIDE", "ASSAULT", "BATTERY", "CRIMINAL SEXUAL ASSAULT", "ROBBERY"]
    df = df.copy()
    df["crime_category"] = df["primary_type"].apply(
        lambda x: "Violent Crime" if x in violent_crimes else "Property Crime"
    )
    df_violent = df[df["crime_category"] == "Violent Crime"].groupby("ward").size().reset_index(name="count")
    df_violent["ward"] = df_violent["ward"].astype(int).astype(str)
    df_property = df[df["crime_category"] == "Property Crime"].groupby("ward").size().reset_index(name="count")
    df_property["ward"] = df_property["ward"].astype(int).astype(str)
    palette_red = bokeh.palettes.Reds[256][::-1]

    def make_map(data, title, max_val):
        return alt.Chart(
            alt.Data(values=chi_map["features"])
        ).mark_geoshape(stroke="white", strokeWidth=0.5).transform_lookup(
            lookup="properties.ward",
            from_=alt.LookupData(data, "ward", ["count"])
        ).encode(
            color=alt.Color(
                "count:Q",
                scale=alt.Scale(range=palette_red, domain=[0, max_val]),
                legend=alt.Legend(title="Crime Count")
            ),
            tooltip=[
                alt.Tooltip("properties.ward:O", title="Ward"),
                alt.Tooltip("count:Q", format=",.0f")
            ]
        ).properties(width=350, height=350, title=title).project(type="mercator")

    return make_map(df_violent, "Violent Crime", df_violent["count"].max()) | \
           make_map(df_property, "Property Crime", df_property["count"].max())


def chart_interactive_ward_map(df, chi_map):
    alt.data_transformers.disable_max_rows()
    df = df.copy()
    df["year"] = pd.to_datetime(df["date"]).dt.year
    df_ward_year = (
        df.groupby(["ward", "year"]).size()
        .reset_index(name="crime_count")
    )
    df_ward_year["ward"] = df_ward_year["ward"].astype(int).astype(str)
    df_ward_year["year"] = df_ward_year["year"].astype(int)

    # Build lookup: {ward: {year: crime_count}}
    lookup = {}
    for _, row in df_ward_year.iterrows():
        lookup.setdefault(row["ward"], {})[row["year"]] = int(row["crime_count"])

    # Embed all years into each feature
    features = copy.deepcopy(chi_map["features"])
    records = []
    for feature in features:
        ward = str(feature["properties"]["ward"])
        for year, count in lookup.get(ward, {}).items():
            rec = copy.deepcopy(feature)
            rec["properties"]["year"] = year
            rec["properties"]["crime_count"] = count
            records.append(rec)

    year_slider = alt.param(
        name="Year",
        bind=alt.binding_range(
            min=int(df_ward_year["year"].min()),
            max=int(df_ward_year["year"].max()),
            step=1
        ),
        value=2001
    )

    return alt.Chart(
        alt.Data(values=records)
    ).mark_geoshape(
        stroke="white", strokeWidth=0.5
    ).transform_filter(
    alt.datum["properties.year"] == year_slider
    ).encode(
        color=alt.Color(
            "properties.crime_count:Q",
            title="Crime Count",
            scale=alt.Scale(scheme="blues")
        ),
        tooltip=[
            alt.Tooltip("properties.ward:N", title="Ward"),
            alt.Tooltip("properties.crime_count:Q", title="Crime Count", format=",.0f"),
            alt.Tooltip("properties.year:Q", title="Year")
        ]
    ).add_params(year_slider).properties(
        width=650, height=650,
        title="Interactive Crime Distribution by Ward and Year"
    ).project(type="mercator")

def chart_arrests_reports(df: pd.DataFrame, socio: pd.DataFrame) -> alt.Chart:
    socio_slim = socio[["community_area", "pct_below_poverty"]]
    df_community = (
        df.groupby("community_area")
        .agg(total_crimes=("id", "count"), total_arrests=("arrest", lambda x: x.eq(True).sum()))
        .reset_index()
        .dropna(subset=["community_area"])
    )
    df_community["community_area"] = df_community["community_area"].astype(int)
    df_community = df_community.merge(socio_slim, on="community_area", how="left")

    df_top15_crimes  = df_community.sort_values("total_crimes",  ascending=False).head(15)
    df_top15_arrests = df_community.sort_values("total_arrests", ascending=False).head(15)

    color_scale = alt.Color(
        "pct_below_poverty:Q",
        scale=alt.Scale(scheme="blues"),
        legend=alt.Legend(title="% Below Poverty")
    )

    chart_crimes = (
        alt.Chart(df_top15_crimes).mark_bar()
        .encode(
            x=alt.X("total_crimes:Q",   title="Total Crimes",  axis=alt.Axis(format="~s")),
            y=alt.Y("community_area:O", sort="-x",             title="Community Area"),
            color=color_scale,
            tooltip=[
                alt.Tooltip("community_area:O",    title="Community Area"),
                alt.Tooltip("total_crimes:Q",      title="Total Crimes",    format=".0f"),
                alt.Tooltip("pct_below_poverty:Q", title="% Below Poverty", format=".1f"),
            ]
        )
        .properties(height=400, title="Top 15 Community Areas by Total Reported Crimes")
    )

    chart_arrests = (
        alt.Chart(df_top15_arrests).mark_bar()
        .encode(
            x=alt.X("total_arrests:Q",  title="Total Arrests", axis=alt.Axis(format="~s")),
            y=alt.Y("community_area:O", sort="-x",             title=""),
            color=color_scale,
            tooltip=[
                alt.Tooltip("community_area:O",    title="Community Area"),
                alt.Tooltip("total_arrests:Q",     title="Total Arrests",   format=".0f"),
                alt.Tooltip("pct_below_poverty:Q", title="% Below Poverty", format=".1f"),
            ]
        )
        .properties(height=400, title="Top 15 Community Areas by Total Arrests")
    )

    return (chart_crimes | chart_arrests).resolve_scale(color="shared")

def chart_income_crime(df: pd.DataFrame, socio: pd.DataFrame) -> alt.Chart:
    socio_slim = socio[["community_area", "per_capita_income"]]
    most_common_crime = (
        df.groupby(["community_area", "primary_type"])
        .size()
        .reset_index(name="crime_count")
        .sort_values("crime_count", ascending=False)
        .drop_duplicates(subset="community_area")
        .rename(columns={"primary_type": "most_common_crime"})
        [["community_area", "most_common_crime"]]
    )
    df_community = (
        df.groupby("community_area")
        .agg(total_crimes=("id", "count"))
        .reset_index()
        .dropna(subset=["community_area"])
    )
    df_community["community_area"] = df_community["community_area"].astype(int)
    df_community = (
        df_community
        .merge(socio_slim, on="community_area", how="left")
        .merge(most_common_crime, on="community_area", how="left")
    )

    df_high_income = df_community.sort_values("per_capita_income", ascending=False).head(15)
    df_low_income  = df_community.sort_values("per_capita_income", ascending=True).head(15)

    color_scale = alt.Color(
        "most_common_crime:N",
        scale=alt.Scale(scheme="tableau20"),
        legend=alt.Legend(title="Most Common Crime")
    )

    chart_high = (
        alt.Chart(df_high_income).mark_bar()
        .encode(
            x=alt.X("total_crimes:Q",   title="Total Crimes",  axis=alt.Axis(format="~s")),
            y=alt.Y("community_area:O", sort="-x",             title="Community Area"),
            color=color_scale,
            tooltip=[
                alt.Tooltip("community_area:O",    title="Community Area"),
                alt.Tooltip("per_capita_income:Q", title="Per Capita Income", format="$,.0f"),
                alt.Tooltip("total_crimes:Q",      title="Total Crimes",      format=".0f"),
                alt.Tooltip("most_common_crime:N", title="Most Common Crime"),
            ]
        )
        .properties(width=400, height=400, title="15 Highest Income Community Areas — Most Common Crime")
    )

    chart_low = (
        alt.Chart(df_low_income).mark_bar()
        .encode(
            x=alt.X("total_crimes:Q",   title="Total Crimes",  axis=alt.Axis(format="~s")),
            y=alt.Y("community_area:O", sort="-x",             title=""),
            color=color_scale,
            tooltip=[
                alt.Tooltip("community_area:O",    title="Community Area"),
                alt.Tooltip("per_capita_income:Q", title="Per Capita Income", format="$,.0f"),
                alt.Tooltip("total_crimes:Q",      title="Total Crimes",      format=".0f"),
                alt.Tooltip("most_common_crime:N", title="Most Common Crime"),
            ]
        )
        .properties(height=400, title="15 Lowest Income Community Areas — Most Common Crime")
    )

    return (chart_high | chart_low).resolve_scale(color="shared")
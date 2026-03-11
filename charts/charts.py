import pandas as pd
import altair as alt
import bokeh.palettes
import copy


def chart_crime_time(df_yearly):
    return alt.Chart(df_yearly).mark_line(point=True).encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("total_crimes:Q", title="Total Crimes", axis=alt.Axis(format='~s')),
        tooltip=[
            alt.Tooltip("year:O", title="Year"),
            alt.Tooltip("total_crimes:Q", title="Total Crimes", format=",.0f")
        ]
    ).properties(height=400, title="Total Reported Crimes in Chicago (2001–Present)")


def chart_crime_type_trends(df_year_type):
    top5 = (
        df_year_type.groupby("primary_type")["crime_count"].sum()
        .sort_values(ascending=False)
        .head(5).index.tolist()
    )
    df = df_year_type[df_year_type["primary_type"].isin(top5)]
    return alt.Chart(df).mark_line(point=True).encode(
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


def chart_top15_communities(df_community):
    df_community = df_community.dropna(subset=["community_area"])
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


def chart_crime_distribution(df_community):
    return alt.Chart(df_community).mark_bar().encode(
        x=alt.X("total_crimes:Q", bin=alt.Bin(maxbins=30), title="Total Crimes per Community Area"),
        y=alt.Y("count():Q", title="Number of Community Areas"),
        tooltip=[alt.Tooltip("count():Q", title="Community Count")]
    ).properties(height=400, title="Distribution of Crime Totals Across Chicago Community Areas")


def chart_arrest_rate_map(df_ward, chi_map):
    alt.data_transformers.disable_max_rows()
    df_ward = df_ward.copy()
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
    ).mark_geoshape(stroke="white", strokeWidth=0.5).encode(
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
    ).properties(width=600, height=600, title="Arrest Rate by Chicago Ward").project(type="mercator")


def chart_violent_vs_property(df_ward_cat, chi_map):
    alt.data_transformers.disable_max_rows()
    df_violent = df_ward_cat[df_ward_cat["crime_category"] == "Violent Crime"][["ward","count"]].copy()
    df_property = df_ward_cat[df_ward_cat["crime_category"] == "Property Crime"][["ward","count"]].copy()
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


def chart_interactive_ward_map(df_ward_year, chi_map):
    alt.data_transformers.disable_max_rows()
    lookup = {}
    for _, row in df_ward_year.iterrows():
        lookup.setdefault(row["ward"], {})[row["year"]] = int(row["crime_count"])

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
        bind=alt.binding_range(min=int(df_ward_year["year"].min()), max=int(df_ward_year["year"].max()), step=1),
        value=2001
    )

    return alt.Chart(
        alt.Data(values=records)
    ).mark_geoshape(stroke="white", strokeWidth=0.5).transform_filter(
        alt.datum["properties.year"] == year_slider
    ).encode(
        color=alt.Color("properties.crime_count:Q", title="Crime Count", scale=alt.Scale(scheme="blues")),
        tooltip=[
            alt.Tooltip("properties.ward:N", title="Ward"),
            alt.Tooltip("properties.crime_count:Q", title="Crime Count", format=",.0f"),
            alt.Tooltip("properties.year:Q", title="Year")
        ]
    ).add_params(year_slider).properties(
        width=650, height=650, title="Interactive Crime Distribution by Ward and Year"
    ).project(type="mercator")

def chart_arrests_reports(df_community_poverty):
    df = df_community_poverty.dropna(subset=["pct_below_poverty"])
    df = df[df["community_area"] != 0]
    df = df.sort_values("total_crimes", ascending=False).head(30)
    base = alt.Chart(df)
    bars_crimes = base.mark_bar(opacity=0.4).encode(
        x=alt.X("community_area:O", sort="-y", title="Community Area"),
        y=alt.Y("total_crimes:Q", title="Count", axis=alt.Axis(format='~s')),
        color=alt.value("gray"),
        tooltip=[
            alt.Tooltip("community_area:O", title="Community Area"),
            alt.Tooltip("total_crimes:Q", title="Total Crimes", format=",.0f"),
        ]
    )
    bars_arrests = base.mark_bar().encode(
        x=alt.X("community_area:O", sort="-y"),
        y=alt.Y("total_arrests:Q"),
        color=alt.Color("pct_below_poverty:Q",
            scale=alt.Scale(scheme="blues"),
            legend=alt.Legend(title="% Below Poverty")
        ),
        tooltip=[
            alt.Tooltip("community_area:O", title="Community Area"),
            alt.Tooltip("total_arrests:Q", title="Total Arrests", format=",.0f"),
            alt.Tooltip("pct_below_poverty:Q", title="% Below Poverty", format=".1f"),
        ]
    )
    return (bars_crimes + bars_arrests).properties(
        height=400,
        title="Top 30 Community Areas: Reported Crimes vs Arrests, Colored by Poverty Rate"
    )


def chart_income_crime(df_income_crime):
    return alt.Chart(df_income_crime).mark_bar().encode(
        x=alt.X("total_crimes:Q", title="Total Crimes", axis=alt.Axis(format='~s')),
        y=alt.Y("community_name:N", sort="-x", title="Community Area"),
        color=alt.Color("primary_type:N", legend=alt.Legend(title="Dominant Crime Type")),
        row=alt.Row("group:N", title=""),
        tooltip=[
            alt.Tooltip("community_name:N", title="Community"),
            alt.Tooltip("total_crimes:Q", title="Total Crimes", format=",.0f"),
            alt.Tooltip("primary_type:N", title="Dominant Crime Type"),
            alt.Tooltip("per_capita_income:Q", title="Per Capita Income", format="$,.0f"),
        ]
    ).properties(
        width=600, height=200,
        title="Dominant Crime Type in Highest vs Lowest Income Community Areas"
    )
    
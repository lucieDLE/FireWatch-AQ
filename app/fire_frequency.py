from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import json
import urllib.request
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.figure_factory as ff
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from src.config import FIRE_PIXEL_PATH, CENTER_LAT, CENTER_LON

# ── Data ─────────────────────────────────────────────────────────────────────

df = pd.read_csv(FIRE_PIXEL_PATH)

with urllib.request.urlopen(
    "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/california-counties.geojson"
) as f:
    ca_geojson = json.load(f)

ca_counties = gpd.GeoDataFrame.from_features(ca_geojson["features"], crs="EPSG:4326")[
    ["name", "geometry"]
]
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df.longitude, df.latitude),
    crs="EPSG:4326",
)
joined = gpd.sjoin(gdf, ca_counties, how="left", predicate="within")
county_counts = (
    joined.groupby("name", dropna=True)["fire_cat"]
    .sum()
    .reset_index(name="fire_score")
    .sort_values("fire_score", ascending=False)
)

# ── Figures ───────────────────────────────────────────────────────────────────

fig_hexbin = ff.create_hexbin_map(
    data_frame=df,
    lat="latitude", lon="longitude",
    nx_hexagon=30,
    opacity=0.6,
    color="fire_cat",
    agg_func=np.sum,
    color_continuous_scale="YlOrRd",
    map_style="open-street-map",
    zoom=5,
    center=dict(lat=CENTER_LAT, lon=CENTER_LON),
    labels={"color": "Fire activity score"},
    title="Fire activity score — hexbin heatmap (weighted by fire category)",
)

fig_bar = px.bar(
    county_counts.head(10),
    x="name", y="fire_score",
    color="fire_score", color_continuous_scale="YlOrRd",
    labels={"name": "County", "fire_score": "Fire activity score"},
    title="Top 10 counties by fire activity score",
)
fig_bar.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)

fig_choropleth = px.choropleth_map(
    county_counts,
    geojson=ca_geojson,
    locations="name",
    featureidkey="properties.name",
    color="fire_score",
    color_continuous_scale="YlOrRd",
    map_style="dark",
    zoom=4.5,
    center={"lat": CENTER_LAT, "lon": CENTER_LON},
    opacity=0.7,
    labels={"fire_score": "Fire activity score"},
    title="Fire activity score by county (weighted by fire category)",
)

# ── Layout ────────────────────────────────────────────────────────────────────

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    fluid=True,
    children=[
        html.H4("Fire Frequency Analysis", className="my-3"),
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=fig_choropleth, style={"height": "480px"}),
                width=6,
            ),
            dbc.Col(
                dcc.Graph(figure=fig_bar, style={"height": "480px"}),
                width=6,
            ),
        ]),
    ],
)

if __name__ == "__main__":
    app.run(debug=True, port=8051)

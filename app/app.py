from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import numpy as np
import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import Point
from shapely.ops import unary_union
import plotly.graph_objects as go
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.config import *
from src.display import *

# ============================================================================
# DATA FUNCTIONS 
# ============================================================================

def compute_cluster_geometry(group):
    polys = [Point(r.longitude, r.latitude).buffer(0.002) for r in group.itertuples()]
    union = unary_union(polys)
    # dilate to fill gaps between satellite pixels, then erode to restore shape
    return union.buffer(0.006).buffer(-0.004)

def geoms_to_lines(gdf_wgs84):
    """Extract polygon exterior rings as flat lat/lon lists with None breaks."""
    lats, lons = [], []
    for geom in gdf_wgs84.geometry:
        polys = geom.geoms if geom.geom_type == 'MultiPolygon' else [geom]
        for poly in polys:
            coords = list(poly.exterior.coords)
            lons += [c[0] for c in coords] + [None]
            lats += [c[1] for c in coords] + [None]
    return lats, lons

def create_fire_gdf_stats(df):
    df = df.loc[df['isFire'] == 1] 

    df_frp_max = df.groupby('acq_date').max('frp').reset_index()[ [ 'acq_date', 'frp']]
    df_frp_max = df_frp_max.rename(columns={'frp':'max_frp'})

    geoms = df.groupby('acq_date').apply(compute_cluster_geometry).rename('geometry').reset_index()

    gdf = gpd.GeoDataFrame(geoms, geometry='geometry', crs='EPSG:4326')
    gdf_proj = gdf.to_crs('EPSG:3310')
    gdf['perimeter_km'] = gdf_proj.geometry.length / 1000
    gdf['area_km2'] = gdf_proj.geometry.area / 1e6

    gdf = gdf.merge(df_frp_max, on='acq_date')

    return gdf

# ============================================================================
# FIGURE FUNCTIONS 
# ============================================================================

def make_aq_hotspot_fig(df_day, site_name, show_colorbar=True, show_legend=True):
    df_day = df_day[df_day['max_AQI'] != 'N/A'].copy()
    colorbar = dict(
        title=dict(text='AQI', font=dict(size=11)),
        thickness=14,
        len=0.5,
        x=1.01,
        y=0.5,
        tickvals=[0, 50, 100, 150, 200, 300, 400],
    ) if show_colorbar else {}
    return go.Scattermapbox(
        lat=df_day['Site Latitude'],
        lon=df_day['Site Longitude'],
        mode='markers',
        name=f'Air Quality Captors',
        marker=dict(
            size=12,
            color=df_day['max_AQI'],
            colorscale=AQI_CMAP,
            cmin=0,
            cmax=400,
            opacity=0.9,
            colorbar=colorbar,
        ),
        customdata=df_day[AQI_REPORT_COLS],
        hovertemplate=AQI_HOVER_TEMPLATE,
        showlegend=show_legend,  # add legend only one time
    )

def make_site_ellipse(df_day, color_line, color_fill, name, padding=0.15):
    lats = df_day['Site Latitude']
    lons = df_day['Site Longitude']

    center_lat, center_lon = lats.mean(), lons.mean()
    r_lat = (lats.max() - lats.min()) / 2 + padding
    r_lon = (lons.max() - lons.min()) / 2 + padding

    theta = np.linspace(0, 2 * np.pi, 120)
    ell_lats = (center_lat + r_lat * np.sin(theta)).tolist()
    ell_lons = (center_lon + r_lon * np.cos(theta)).tolist()

    return go.Scattermapbox(
        lat=ell_lats,
        lon=ell_lons,
        mode='lines',
        fill='toself',
        fillcolor=color_fill,
        line=dict(color=color_line, width=2),
        name=name,
        hoverinfo='skip',
        showlegend=True,
    )

def make_aq_time_series(df, sites, site_name):

    fig = go.Figure()
    for site_id in sites:
        df_site = df.loc[df['Site ID'] == site_id] # Long Beach
        fig.add_trace(go.Scatter(x=df_site['Date'], y=df_site['max_AQI'], name=df_site.iloc[0]['Local Site Name']))


    for y0, y1, color in AQI_BANDS_COLOR:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=color, line_width=0, layer='below')


    fig.update_layout(
        title=dict(text=f'Air Quality Index at Selected Sites near: {site_name}'),
        xaxis=dict(title_text="Date"),
        yaxis=dict(title_text="Air Quality Index (AQI)"),
        legend=dict(title_text='Monitored Sites',
                    orientation="h",
                    yanchor="bottom",
                    y=-0.35,
                    xanchor="center",
                    x=0.5,
                    maxheight=0.1,
                    ),

    )
    return fig

def make_fire_perimeter_plot(gdf):
    # if there is no fire
    if gdf.empty:
        return go.Scattermapbox(lat=[], lon=[], mode='lines', name='Fire perimeter', showlegend=True)

    perim_lats, perim_lons = geoms_to_lines(gdf)
    n_pts = len(perim_lats)
    cd_vals = np.tile(gdf[FIRE_REPORT_COLS].round(1).values[0], (n_pts, 1))

    return go.Scattermapbox(
        lat=perim_lats,
        lon=perim_lons,
        mode='lines',
        fill='toself',
        fillcolor='rgba(255, 100, 0, 0.15)',
        line=dict(width=1.5, color='rgba(255, 100, 0, 0.85)'),
        name='Fire perimeter',
        customdata=cd_vals,
        hovertemplate=FIRE_HOVER_TEMPLATE,
    )

def make_burning_area_plot(gdf):

    return go.Figure([
                        go.Scatter( x=gdf['acq_date'], y=gdf['area_km2'], name = 'Burning Area (km2)'),
                        go.Scatter( x=gdf['acq_date'], y=gdf['perimeter_km'], name= 'Fire Perimeter (km)'),
                    ])


# ============================================================================
# DATA LOADING
# ============================================================================

df_aqi = pd.read_csv(AIR_QUALITY_REPORT_PATH)
df_fire = pd.read_csv(FIRE_PIXEL_PATH)

site_1 = WATCH_SITES['Garnet - Site 1']
site_2 = WATCH_SITES['Garnet - Site 2'] 


df_fire_event = df_fire.loc[ (df_fire['acq_date'] > EVENT_START) & (df_fire['acq_date'] < EVENT_END) ]

df_aqi_event = df_aqi.loc[ (df_aqi['Date'] > EVENT_START) & (df_aqi['Date'] < EVENT_END) ]
df_aqi_event = df_aqi_event.fillna('N/A')

df_event_site_1 = df_aqi_event.loc[df_aqi_event['Site ID'].isin(site_1)].copy()
df_event_site_2 = df_aqi_event.loc[df_aqi_event['Site ID'].isin(site_2)].copy()

unique_dates = sorted(df_aqi_event['Date'].unique())

df_fire_event = df_fire_event.loc[ (df_fire_event['latitude'] > FIRE_LAT[0]) & (df_fire_event['latitude'] < FIRE_LAT[1]) ]
df_fire_event = df_fire_event.loc[ (df_fire_event['longitude'] > FIRE_LON[0]) & (df_fire_event['longitude'] < FIRE_LON[1]) ]

gdf = create_fire_gdf_stats(df_fire_event)

# ============================================================================
#  BUILD FIGURES
# ============================================================================

# user selected or frame 
SELECTED_DAY = '2025-09-08'

gdf_fire_day = gdf.loc[gdf['acq_date'] == SELECTED_DAY]
geojson_fire_dict = json.loads(gdf_fire_day.to_json())

df_day_site_1 = df_event_site_1[df_event_site_1['Date'] == SELECTED_DAY]
df_day_site_2 = df_event_site_2[df_event_site_2['Date'] == SELECTED_DAY]


# timeseries plots
ts_site_1= make_aq_time_series(df_event_site_1, site_1, 'Fresno Area')
ts_site_2 = make_aq_time_series(df_event_site_2, site_2, 'Sierra National Forest - EAST')
fire_perimeter = make_burning_area_plot(gdf)

aq_fire_overlay = go.Figure(data=[
                                make_site_ellipse(df_day_site_1, 'rgba(50,160,50,0.9)', 'rgba(50,160,50,0.12)',
                                                'Monitoring Site 1: Fresno', padding=0.2),
                                make_site_ellipse(df_day_site_2, 'rgba(20,60,140,0.9)', 'rgba(20,60,140,0.08)',
                                                'Monitoring Site 2: Sierra National Forest (EAST)', padding=0.3),
                                make_aq_hotspot_fig(df_day_site_1, 'Fresno', show_colorbar=True, show_legend=True),
                                make_aq_hotspot_fig(df_day_site_2, 'Sierra National Forest (EAST)', show_colorbar=False, show_legend=False),
                                make_fire_perimeter_plot(gdf_fire_day),
                                ],)


aq_fire_overlay.update_layout(
                            height=500, 
                            width= 800,
                            title=dict(
                                text=f'Fire Perimeter & Air Quality — {SELECTED_DAY}',
                                font=dict(size=15), x=0.5, xanchor='center',
                            ),
                            mapbox=dict(
                                style='carto-positron',
                                layers=[dict(
                                    sourcetype='geojson',
                                    source=geojson_fire_dict,
                                    type='fill',
                                    color='rgba(255, 100, 0, 0.2)',
                                    below='traces',
                                )],
                                center=dict(lat=CENTER_LAT, lon=CENTER_LON),
                                zoom=7,
                            ),
                            margin=dict(l=0, r=90, t=50, b=10),
                            legend=dict(
                                bgcolor='rgba(255, 255, 255, 0.85)',
                                bordercolor='rgba(180, 180, 180, 0.8)',
                                borderwidth=1,
                                x=0.01,
                                y=0.99,
                                xanchor='left',
                                yanchor='top',
                                font=dict(size=12),
                                itemsizing='constant',
                            ),
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

if __name__ == '__main__':
    app.run(debug=True)

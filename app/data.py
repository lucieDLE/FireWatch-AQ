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
import plotly.express as px
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.config import *
from src.display import *
from figures import *

# ============================================================================
# DATA FUNCTIONS 
# ============================================================================

def compute_cluster_geometry(group):
    polys = [Point(r.longitude, r.latitude).buffer(0.002) for r in group.itertuples()]
    union = unary_union(polys)
    # dilate to fill gaps between satellite pixels, then erode to restore shape
    return union.buffer(0.006).buffer(-0.004)


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

gdf_fire_day = gdf.loc[gdf['acq_date'] == SELECTED_DAY]
geojson_fire_dict = json.loads(gdf_fire_day.to_json())

df_day_site_1 = df_event_site_1[df_event_site_1['Date'] == SELECTED_DAY]
df_day_site_2 = df_event_site_2[df_event_site_2['Date'] == SELECTED_DAY]
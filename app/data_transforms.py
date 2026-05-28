from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union

from src.config import (
    POLLUTANT_STANDARD_NAMES, POLLUTATANT_SAMPLE_DURATION,
    EVENT_START, EVENT_END, FIRE_LAT, FIRE_LON, SELECTED_DAY,
)
from src.display import WATCH_SITES
from data_loaders import df_aqi, df_fire, df_aqr_annual, ca_geojson


# ============================================================================
# Geometry helpers
# ============================================================================

def compute_cluster_geometry(group):
    polys = [Point(r.longitude, r.latitude).buffer(0.002) for r in group.itertuples()]
    union = unary_union(polys)
    # dilate to fill gaps between satellite pixels, then erode to restore shape
    return union.buffer(0.006).buffer(-0.004)


def create_fire_gdf_stats(df):
    df = df.loc[df['isFire'] == 1]

    df_frp_max = df.groupby('acq_date').max('frp').reset_index()[['acq_date', 'frp']]
    df_frp_max = df_frp_max.rename(columns={'frp': 'max_frp'})

    geoms = df.groupby('acq_date').apply(compute_cluster_geometry).rename('geometry').reset_index()

    gdf = gpd.GeoDataFrame(geoms, geometry='geometry', crs='EPSG:4326')
    gdf_proj = gdf.to_crs('EPSG:3310')
    gdf['perimeter_km'] = gdf_proj.geometry.length / 1000
    gdf['area_km2'] = gdf_proj.geometry.area / 1e6

    gdf = gdf.merge(df_frp_max, on='acq_date')
    return gdf


# ============================================================================
# Panel 1: AQ Stats
# ============================================================================

df_aqr_annual = df_aqr_annual.loc[
    (df_aqr_annual['Pollutant Standard'].isin(POLLUTANT_STANDARD_NAMES)) &
    (df_aqr_annual['Sample Duration'].isin(POLLUTATANT_SAMPLE_DURATION))
]
df_aqr_annual = df_aqr_annual.loc[df_aqr_annual['State Name'] != 'Country Of Mexico']

df_county_aqr_annual = df_aqr_annual[[
    'Observation Count',
    'County Name',
    'Primary Exceedance Count',
    'Secondary Exceedance Count',
    'State Name',
    'Longitude',
    'Latitude',
    'Parameter Name',
]]

df_county_aqr_annual = df_county_aqr_annual.groupby(['County Name', 'State Name']).agg(
    primary_exceedance=('Primary Exceedance Count', 'sum'),
    observation=('Observation Count', 'sum'),
    state_name=('State Name', 'min'),
    latitude=('Latitude', 'mean'),
    longitude=('Longitude', 'mean'),
).reset_index()
df_county_aqr_annual['captor_exceeded_ratio'] = (
    df_county_aqr_annual['primary_exceedance'] / df_county_aqr_annual['observation']
)

df_state_aqr_annual = df_county_aqr_annual.groupby('state_name').agg(
    primary_exceedance=('primary_exceedance', 'sum'),
    observation=('observation', 'sum'),
    latitude=('latitude', 'mean'),
    longitude=('longitude', 'mean'),
).reset_index()
df_state_aqr_annual['captor_exceeded_ratio'] = (
    df_state_aqr_annual['primary_exceedance'] / df_state_aqr_annual['observation']
)

df_cleanest_states = df_state_aqr_annual.sort_values(
    by=['captor_exceeded_ratio', 'observation'], ascending=[True, False]
)[:3]['state_name']
df_worst_states = df_state_aqr_annual.sort_values(
    by=['primary_exceedance', 'observation'], ascending=[False, True]
)[:3]['state_name']

state_list = df_cleanest_states.to_list() + df_worst_states.to_list()

df_annual_stats = df_aqr_annual[[
    '1st Max Value', '2nd Max Value', '3rd Max Value', '4th Max Value',
    '99th Percentile', '98th Percentile', '95th Percentile',
    'Arithmetic Mean', 'Arithmetic Standard Dev',
    '90th Percentile', '75th Percentile', '50th Percentile', '10th Percentile',
    'State Name', 'Parameter Name',
]]
df_annual_stats['q1'] = (
    df_annual_stats['10th Percentile']
    + 0.375 * (df_annual_stats['50th Percentile'] - df_annual_stats['10th Percentile'])
)


# ============================================================================
# Panel 2: Fire Stats
# ============================================================================

df_fire = df_fire.loc[(df_fire['acq_date'] >= '2025-01-01') & (df_fire['acq_date'] < '2026-01-01')]

df_biggest_fire = (
    df_fire[['poly_IncidentName', 'poly_GISAcres', 'attr_POOCounty', 'attr_FireDiscoveryDateTime','endFire']]
    .groupby('poly_IncidentName')
    .agg(   
        acres=('poly_GISAcres', 'max'), 
        county=('attr_POOCounty', 'min'),
        start_date = ('attr_FireDiscoveryDateTime', 'max'),
        end_date = ('endFire', 'max'),
        )
    .reset_index()
    .sort_values(by='acres', ascending=False)
    .head(8)
)
df_biggest_fire['label'] = df_biggest_fire['poly_IncidentName'] + '<br>' + df_biggest_fire['county']

POLLUTANT_COL_MAP = {
    'PM2.5':  'Daily AQI Value_PM2.5',
    'PM10':   'Daily AQI Value_PM10',
    'Ozone':  'Daily AQI Value_O3',
    'NO2':    'Daily AQI Value_NO2',
}


def compute_aqi_quantiles(pollutant_col):
    grouped = df_aqi[[pollutant_col, 'Date']].groupby('Date')
    df_q = grouped.quantile(0.25).rename(columns={pollutant_col: 'Q1'}).reset_index()
    df_q['Q2']  = grouped.quantile(0.50)[pollutant_col].values
    df_q['Q3']  = grouped.quantile(0.75)[pollutant_col].values
    df_q['Q99'] = grouped.quantile(0.99)[pollutant_col].values
    for col in ['Q1', 'Q2', 'Q3', 'Q99']:
        df_q[f'{col}_smooth'] = df_q[col].rolling(window=3, center=True).mean()
    return df_q


df_aq_quantile = compute_aqi_quantiles(POLLUTANT_COL_MAP['PM2.5'])


# ============================================================================
# Panel 4: Event Dive
# ============================================================================

site_1 = WATCH_SITES['Garnet - Site 1']
site_2 = WATCH_SITES['Garnet - Site 2']

df_fire_event = df_fire.loc[(df_fire['acq_date'] > EVENT_START) & (df_fire['acq_date'] < EVENT_END)]

df_aqi_event = df_aqi.loc[(df_aqi['Date'] > EVENT_START) & (df_aqi['Date'] < EVENT_END)]
df_aqi_event = df_aqi_event.fillna('N/A')

df_event_site_1 = df_aqi_event.loc[df_aqi_event['Site ID'].isin(site_1)].copy()
df_event_site_2 = df_aqi_event.loc[df_aqi_event['Site ID'].isin(site_2)].copy()

unique_dates = sorted(df_aqi_event['Date'].unique())

df_fire_event = df_fire_event.loc[
    (df_fire_event['latitude'] > FIRE_LAT[0]) & (df_fire_event['latitude'] < FIRE_LAT[1])
]
df_fire_event = df_fire_event.loc[
    (df_fire_event['longitude'] > FIRE_LON[0]) & (df_fire_event['longitude'] < FIRE_LON[1])
]

gdf = create_fire_gdf_stats(df_fire_event)

gdf_fire_day = gdf.loc[gdf['acq_date'] == SELECTED_DAY]
geojson_fire_dict = json.loads(gdf_fire_day.to_json())

df_day_site_1 = df_event_site_1[df_event_site_1['Date'] == SELECTED_DAY]
df_day_site_2 = df_event_site_2[df_event_site_2['Date'] == SELECTED_DAY]

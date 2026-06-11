import path_setup  # noqa: F401

import os
import json
from functools import lru_cache
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union

os.environ.setdefault('PROJ_NETWORK', 'OFF')

from src.config import (
    POLLUTANT_STANDARD_NAMES, POLLUTANT_SAMPLE_DURATION,
    FIRE_RAW_PATH,
)
from src.display import WATCH_SITES, FIRE_WATCH_SITES, STATE_NAME_TO_CODE
from data_loaders import df_aqi, df_fire, df_aqr_annual, ca_geojson


import numpy as np
# ============================================================================
# Geometry helpers
# ============================================================================

def compute_cluster_geometry(group):
    polys = [Point(r.longitude, r.latitude).buffer(0.002) for r in group.itertuples()]
    union = unary_union(polys)
    # dilate to fill gaps between satellite pixels, then erode to restore shape
    return union.buffer(0.006)


def compute_burnt_area_gdf(gdf, selected_day):
    """Union of all fire perimeters from days strictly before selected_day."""
    gdf_before = gdf.loc[gdf['acq_date'] < selected_day]
    if gdf_before.empty:
        return gdf.iloc[:0]
    burnt_union = gdf_before.geometry.unary_union
    gdf_union = gpd.GeoDataFrame(geometry=[burnt_union], crs='EPSG:4326')
    proj = gdf_union.to_crs('EPSG:3310')
    return gpd.GeoDataFrame(
        {'acq_date': [selected_day],
         'perimeter_km': [round(proj.geometry.length.iloc[0] / 1000, 1)],
         'area_km2':     [round(proj.geometry.area.iloc[0]   / 1e6,  1)],
         'max_frp':      [round(gdf_before['max_frp'].max(), 1)]},
        geometry=[burnt_union], crs='EPSG:4326'
    )


def create_fire_gdf_stats(df):
    df = df.loc[df['isFire'] == 1]

    df_frp_max = df.groupby('acq_date').max('frp').reset_index()[['acq_date', 'frp']]
    df_frp_max = df_frp_max.rename(columns={'frp': 'max_frp'})

    geoms = df.groupby('acq_date').apply(compute_cluster_geometry, include_groups=False).rename('geometry').reset_index()

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
    (df_aqr_annual['Sample Duration'].isin(POLLUTANT_SAMPLE_DURATION))
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

list_best_codes  = [STATE_NAME_TO_CODE[s] for s in df_cleanest_states if s in STATE_NAME_TO_CODE]
list_worst_codes = [STATE_NAME_TO_CODE[s] for s in df_worst_states  if s in STATE_NAME_TO_CODE]

df_annual_stats = df_aqr_annual[[
    '1st Max Value', '2nd Max Value', '3rd Max Value', '4th Max Value',
    '99th Percentile', '98th Percentile', '95th Percentile',
    'Arithmetic Mean', 'Arithmetic Standard Dev',
    '90th Percentile', '75th Percentile', '50th Percentile', '10th Percentile',
    'State Name', 'Parameter Name',
]].copy()
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
)
df_biggest_fire['label'] = df_biggest_fire['poly_IncidentName'] + '<br>' + df_biggest_fire['county']

POLLUTANT_COL_MAP = {
    'PM2.5':  'Daily AQI Value_PM2.5',
    'PM10':   'Daily AQI Value_PM10',
    'Ozone':  'Daily AQI Value_O3',
    'NO2':    'Daily AQI Value_NO2',
}


# ----------------------------------------------------------------------------
# Misclassification examples (Behind the Data tab)
# ----------------------------------------------------------------------------
# EPA reports a single number = the worst individual pollutant (max_AQI). The
# custom sum_AQI also uses secondary exceedances, so on some days
# the site has a higher health category than the EPA number suggests.

_AQI_CATEGORIES = [
    (50,  'Good'),
    (100, 'Moderate'),
    (150, 'Unhealthy for SG'),
    (200, 'Unhealthy'),
    (300, 'Very Unhealthy'),
    (500, 'Hazardous'),
]


def _aqi_category(value):
    for hi, label in _AQI_CATEGORIES:
        if value <= hi:
            return label


def compute_misclassification_examples(df, max_days=6):
    """
    Find real days where sum_AQI pushes a site into 2 categories above
    than max_AQI.
    """
    groups = []
    for threshold in [100, 150]:
        df_exceed = df.loc[(df['max_AQI'] <= threshold) & (df['sum_AQI'] > threshold+50)]
        if df_exceed.empty:
            continue
        df_exceed = df_exceed.sort_values(by='hidden_pollution', ascending=False).head(max_days)

        sites = []
        for (site, county), g in df_exceed.groupby(['Local Site Name', 'County'], sort=False):
            days = []
            for idx, row in g.iterrows():
                pollutants = []
                for name, col in POLLUTANT_COL_MAP.items():
                    val = pd.to_numeric(pd.Series([row.get(col)]), errors='coerce').iloc[0]
                    pollutants.append({
                        'name':  name,
                        'value': round(float(val)) if pd.notna(val) else None,
                    })
                days.append(pollutants)
            sites.append({'site': site, 'county': county, 'days': days})

        groups.append({
            'epa_label':       _aqi_category(threshold),
            'epa_value':       df_exceed['max_AQI'].max(),
            'sum_aqi_value': df_exceed['sum_AQI'].max(),
            'sum_aqi_label': _aqi_category(df_exceed['sum_AQI'].max()),
            'n_days':          len(df_exceed),
            'sites':           sites,
        })
    return groups


misclassification_examples = compute_misclassification_examples(df_aqi)


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
# Panel 4: Event Dive — From Selected Event
# ============================================================================
# give us a 4 days to see the baseline before fire 
df_biggest_fire['buffer_start_day'] = pd.to_datetime(df_biggest_fire['start_date']) - pd.Timedelta(days=4)

FIRE_OPTIONS = [name for name in FIRE_WATCH_SITES if name in df_biggest_fire['poly_IncidentName'].values]
DEFAULT_FIRE = FIRE_OPTIONS[1]

_event_cache: dict = {}

def get_event_data(fire_name: str) -> dict:
    """Compute all Panel-4 variables for a given fire name. Results are cached."""
    if fire_name in _event_cache:
        return _event_cache[fire_name]

    row = df_biggest_fire[df_biggest_fire['poly_IncidentName'] == fire_name].iloc[0]
    watch_site_list = FIRE_WATCH_SITES[fire_name]

    # merge knonw fire complex
    if fire_name == 'PALISADES':
        df_fire_event = df_fire.loc[df_fire['poly_IncidentName'].isin(['PALISADES', 'Eaton', 'Hughes'])]
    # elif fire_name == 'Garnet':
    #     df_fire_event = df_fire.loc[df_fire['poly_IncidentName'].isin(['Garnet', 'SALT 14-2'])]
    else:
        df_fire_event = df_fire.loc[df_fire['poly_IncidentName'] == fire_name]

    event_start = row['buffer_start_day']
    last_pixel_date = pd.to_datetime(df_fire_event['acq_date'].max())
    event_end = (last_pixel_date + pd.Timedelta(days=7)).strftime('%Y-%m-%d')
    fire_lat = (df_fire_event['latitude'].min(), df_fire_event['latitude'].max())
    fire_lon = (df_fire_event['longitude'].min(), df_fire_event['longitude'].max())

    df_aqi_event = df_aqi.loc[
        (df_aqi['Date'] > str(event_start)) & (df_aqi['Date'] < event_end)
    ].copy().fillna('N/A')

    # focus on Pm 2,5 as previous panel shows that fire have a higher impact on PM2.5
    df_aqi_event['max_AQI'] = df_aqi_event['Daily AQI Value_PM2.5']

    site_1_ids = WATCH_SITES[watch_site_list[0]]
    site_2_ids = WATCH_SITES[watch_site_list[1]]

    df_event_site_1 = df_aqi_event.loc[df_aqi_event['Site ID'].isin(site_1_ids)].copy()
    df_event_site_2 = df_aqi_event.loc[df_aqi_event['Site ID'].isin(site_2_ids)].copy()
    df_event_site_1['Site Name'] = watch_site_list[0]
    df_event_site_2['Site Name'] = watch_site_list[1]

    # Compute bounding box across fire pixels + all monitoring sites
    site_lats = (df_event_site_1['Site Latitude'].dropna().tolist() +
                 df_event_site_2['Site Latitude'].dropna().tolist())
    site_lons = (df_event_site_1['Site Longitude'].dropna().tolist() +
                 df_event_site_2['Site Longitude'].dropna().tolist())
    all_lats = site_lats + [fire_lat[0], fire_lat[1]]
    all_lons = site_lons + [fire_lon[0], fire_lon[1]]
    _pad = 0.35
    _min_lat, _max_lat = min(all_lats) - _pad, max(all_lats) + _pad
    _min_lon, _max_lon = min(all_lons) - _pad, max(all_lons) + _pad
    map_center_lat = (_min_lat + _max_lat) / 2
    map_center_lon = (_min_lon + _max_lon) / 2

    event_dates = sorted(df_aqi_event['Date'].unique())
    selected_day = event_dates[0] if event_dates else None

    gdf_event = create_fire_gdf_stats(df_fire_event)
    gdf_fire_day = gdf_event.loc[gdf_event['acq_date'] == selected_day] if selected_day else gdf_event.iloc[:0]
    
    gdf_burnt_area = compute_burnt_area_gdf(gdf_event, selected_day) if selected_day else gdf_event.iloc[:0]
    geojson_burnt_dict = json.loads(gdf_burnt_area.to_json())

    geojson_fire_dict = json.loads(gdf_fire_day.to_json())

    df_day_site_1 = df_event_site_1[df_event_site_1['Date'] == selected_day].copy() if selected_day else df_event_site_1.iloc[:0]
    df_day_site_2 = df_event_site_2[df_event_site_2['Date'] == selected_day].copy() if selected_day else df_event_site_2.iloc[:0]

    result = dict(
        site_1=site_1_ids,
        site_2=site_2_ids,
        site_name_1=watch_site_list[0],
        site_name_2=watch_site_list[1],
        df_event_site_1=df_event_site_1,
        df_event_site_2=df_event_site_2,
        EVENT_START=event_start,
        EVENT_END=event_end,
        FIRE_LAT=fire_lat,
        FIRE_LON=fire_lon,
        event_dates=event_dates,
        SELECTED_DAY=selected_day,
        gdf=gdf_event,
        gdf_fire_day=gdf_fire_day,
        geojson_fire_dict=geojson_fire_dict,

        gdf_burnt_area=gdf_burnt_area,
        geojson_burnt_dict=geojson_burnt_dict,

        map_center_lat=map_center_lat,
        map_center_lon=map_center_lon,

        df_day_site_1=df_day_site_1,
        df_day_site_2=df_day_site_2,
    )
    _event_cache[fire_name] = result
    return result

# Expose initial event variables at module level for layout.py initial render
_ev = get_event_data(DEFAULT_FIRE)
site_1            = _ev['site_1']
site_2            = _ev['site_2']
site_name_1       = _ev['site_name_1']
site_name_2       = _ev['site_name_2']
df_event_site_1   = _ev['df_event_site_1']
df_event_site_2   = _ev['df_event_site_2']
EVENT_START       = _ev['EVENT_START']
EVENT_END         = _ev['EVENT_END']
FIRE_LAT          = _ev['FIRE_LAT']
FIRE_LON          = _ev['FIRE_LON']
event_dates       = _ev['event_dates']
SELECTED_DAY      = _ev['SELECTED_DAY']
gdf               = _ev['gdf']
gdf_fire_day      = _ev['gdf_fire_day']
geojson_fire_dict = _ev['geojson_fire_dict']
gdf_burnt_area    = _ev['gdf_burnt_area']
geojson_burnt_dict= _ev['geojson_burnt_dict']
map_center_lat    = _ev['map_center_lat']
map_center_lon    = _ev['map_center_lon']
df_day_site_1     = _ev['df_day_site_1']
df_day_site_2     = _ev['df_day_site_2']

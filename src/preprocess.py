import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union
from src.config import (
     FIRE_RAW_PATH, 
     OZONE_PATH, NITROGEN_DIOXIDE_PATH, CARBON_MONOXIDE_PATH, PM25_PATH,
     FIRE_EVENTS_PATH, FIRE_EVENTS_GDF_PATH, AIR_QUALITY_REPORT_PATH,
)
    

## preprocessing variables
AQI_DROP_COLUMNS = ['Source', 
                    'POC', 
                    'Local Site Name', 
                    'Daily Obs Count', 
                    'Percent Complete', 
                    'AQS Parameter Code', 
                    'AQS Parameter Description',
                    "Method Code",
                    "Method Description",
                    "County FIPS Code",
                    "State FIPS Code",
                    "CBSA Code",
                    'CBSA Name', 
                    'CBSA Code', 
                    ]

AQI_MERGE_COLUMNS = ['Date', 
                    'Site ID', 
                    'County', 
                    'State',
                    'Site Longitude',
                    'Site Latitude'
                    ]

def compute_cluster_geometry(group):
    polys = [Point(r.longitude, r.latitude).buffer(0.002) for r in group.itertuples()]
    union = unary_union(polys)
    # dilate to fill gaps between satellite pixels, then erode to restore shape
    return union.buffer(0.006).buffer(-0.004)


def get_max_AQI(row):
    val_max = row[['Daily AQI Value_PM2.5', 'Daily AQI Value_O3', 'Daily AQI Value_NO2', 'Daily AQI Value_CO']].max()
    return val_max

### ------ step 1: fire preprocess ------ ###

df_fire = pd.read_csv(FIRE_RAW_PATH)

# 1.a remove non-vegetation fire + low confidence datapoints
df_fire_cleaned = df_fire.loc[ df_fire['type']==0]
df_fire_cleaned = df_fire_cleaned.loc[ df_fire['confidence'] != 'l']


# 1.b  cluster data into spatial location and time --> gather into events

# Pass 1 — spatial clustering on full year (eps ~5km)
spatial = DBSCAN(eps=0.05, min_samples=3).fit(df_fire_cleaned[['latitude', 'longitude']])
df_fire_cleaned['spatial_cluster'] = spatial.labels_

# Pass 2 — within each spatial cluster, split by gaps > 5 days
def assign_time_subgroup(group, max_gap_days=4):
    dates = pd.to_datetime(group['acq_date']).sort_values()
    gap = dates.diff().dt.days.fillna(0)
    return (gap > max_gap_days).cumsum().rename('time_subgroup')

df_fire_cleaned['time_subgroup'] = (
    df_fire_cleaned[df_fire_cleaned['spatial_cluster'] >= 0]
    .groupby('spatial_cluster', group_keys=False)
    .apply(assign_time_subgroup)
)

# Combine into a single event ID
df_fire_cleaned['event_id'] = (
    df_fire_cleaned['spatial_cluster'].astype(str) + '_' +
    df_fire_cleaned['time_subgroup'].astype(str)
)


fire_events = (
    # if cluster are <=0, they are just one pixel -> remove them
    df_fire_cleaned[df_fire_cleaned['spatial_cluster'] >= 0]
    .groupby('event_id')
    .agg(
        pixel_count = ('frp', 'count'),
        latitude = ('latitude', 'mean'),
        longitude = ('longitude', 'mean'),
        mean_frp = ('frp', 'mean'),
        max_frp = ('frp', 'max'),
        first_seen = ('acq_date', 'min'),
        last_seen = ('acq_date', 'max'),
    )
    .reset_index())


# 1.c compute durations of event
fire_events['duration_days'] = ( 
    pd.to_datetime(fire_events['last_seen']) - pd.to_datetime(fire_events['first_seen'])
    ).dt.days + 1



# 1.d compute perimeter of fire and burnt area estimates
geoms = (
    df_fire_cleaned[df_fire_cleaned['spatial_cluster'] >= 0]
    .groupby('event_id')
    .apply(compute_cluster_geometry)
    .rename('geometry')
    .reset_index()
)

gdf = gpd.GeoDataFrame(geoms, geometry='geometry', crs='EPSG:4326')
gdf_proj = gdf.to_crs('EPSG:3310')
gdf['perimeter_km'] = gdf_proj.geometry.length / 1000
gdf['area_km2']= gdf_proj.geometry.area / 1e6

gdf.to_file(FIRE_EVENTS_GDF_PATH, driver="GeoJSON")

# merge everything
fire_events = fire_events.merge(gdf[['event_id', 'perimeter_km', 'area_km2']], on='event_id')

fire_events.to_csv(FIRE_EVENTS_PATH)


## step 2: Air quality report aggregation

# step 2.1 read all files
df_o3= pd.read_csv(OZONE_PATH)
df_o3 = df_o3.drop(columns=AQI_DROP_COLUMNS, errors='ignore')

df_pm25 = pd.read_csv(PM25_PATH)
df_pm25 = df_pm25.drop(columns=AQI_DROP_COLUMNS, errors='ignore')

df_no2 = pd.read_csv(NITROGEN_DIOXIDE_PATH)
df_no2 = df_no2.drop(columns=AQI_DROP_COLUMNS, errors='ignore')


df_co = pd.read_csv(CARBON_MONOXIDE_PATH)
df_co = df_co.drop(columns=AQI_DROP_COLUMNS, errors='ignore')


# step 2.2 : merge data
df_all = df_pm25.merge(df_o3, on=AQI_MERGE_COLUMNS, how='outer', suffixes=['_PM2.5', '_O3']
                        ).merge(df_no2, on=AQI_MERGE_COLUMNS, how='outer'
                        ).merge(df_co, on=AQI_MERGE_COLUMNS, how='outer', suffixes=['_NO2', '_CO']
                        )

# step 2.3 : compute and filter on missing values
df_all['n_missing_values'] = df_all.apply(lambda row: row.isnull().sum(), axis=1)
df_aqi = df_all.loc[df_all['n_missing_values'] <= 6].reset_index() # keep rows where at least 2 metrics

# step 2.4 : compute global AQI value based on max AQI_pollutant value
df_aqi['max_AQI'] = df_aqi.apply(lambda row: get_max_AQI(row), axis =1 )

df_aqi['Units_PM2.5'] = 'ug/m3 LC'
df_aqi['Units_O3'] = 'ppm'
df_aqi['Units_NO2'] = 'ppb'
df_aqi['Units_CO'] = 'ppm'

df_aqi = df_aqi.fillna('N/A')

df_aqi.to_csv(AIR_QUALITY_REPORT_PATH)
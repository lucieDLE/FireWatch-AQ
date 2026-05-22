import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
import argparse
import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union
from src.config import (
     FIRE_RAW_PATH, FIRE_PIXEL_PATH,
     OZONE_PATH, NITROGEN_DIOXIDE_PATH, CARBON_MONOXIDE_PATH, PM25_PATH,
     FIRE_EVENTS_PATH, AIR_QUALITY_REPORT_PATH,
)
    

## preprocessing variables
AQI_DROP_COLUMNS = ['Source', 
                    'POC', 
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
                    'Local Site Name', 
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

def assign_time_subgroup(group, max_gap_days=4):
    dates = pd.to_datetime(group['acq_date']).sort_values()
    gap = dates.diff().dt.days.fillna(0)
    return (gap > max_gap_days).cumsum().rename('time_subgroup')

def is_fire(row):
    # based on https://appliedsciences.nasa.gov/sites/default/files/2023-03/D1P5_FireDetection_Final.pdf
    # see slide 9-10 for classification
    bool_fire = ((row['daynight'] == 'D') & (row['diff'] > 25) ) | ((row['daynight'] == 'N') & (row['diff'] > 10) )
    return int(bool_fire)


def clean_fire_data(df, max_px_thr=0.6, min_fpr_thr=5):
    df_cleaned = df.copy()
    
    # a. remove loq confidence vals
    df_cleaned = df.loc[df['confidence'] != 'l']
    print(f"confidence filtering step: {len(df) - len(df_cleaned)} removed")
    tmp_df_len = len(df_cleaned)

    # b. keep only vegetation fires
    df_cleaned = df_cleaned.loc[df_cleaned['type'] == 0]
    print(f"type filtering step: {tmp_df_len - len(df_cleaned)} removed")
    tmp_df_len = len(df_cleaned)

    # c. remove loq confidence vals
    df_cleaned = df_cleaned.loc[df_cleaned['isFire'] == 1]
    print(f"Fire filtering step: {len(df) - tmp_df_len} removed")
    tmp_df_len = len(df_cleaned)

    # d. frp threshold
    df_cleaned = df_cleaned.loc[df_cleaned['frp'] > min_fpr_thr]
    print(f"FRP filtering step: {tmp_df_len - len(df_cleaned)} removed")
    tmp_df_len = len(df_cleaned)
    
    # e. scan/track pixels threshold
    df_cleaned = df_cleaned.loc[(df_cleaned['scan'] < max_px_thr) & (df_cleaned['track'] < max_px_thr)]
    print(f"pixel size filtering step: {tmp_df_len - len(df_cleaned)} removed")
    tmp_df_len = len(df_cleaned)

    # # f. spatial duplication
    df_cleaned['acq_datetime'] = df_cleaned['acq_date'].astype(str).str.replace('-','')
    df_cleaned['acq_datetime'] = df_cleaned['acq_datetime'] + df_cleaned['acq_time'].astype(str).str.zfill(4)
    df_cleaned['acq_datetime'] = pd.to_datetime(df_cleaned['acq_datetime'], format='%Y%m%d%H%M')

    df_cleaned['lat_r'] = df_cleaned['latitude'].round(3)   # ~111m per 0.001°
    df_cleaned['lon_r'] = df_cleaned['longitude'].round(3)
    df_cleaned['time_bin'] = df_cleaned['acq_datetime'].dt.floor('12h')

    df_cleaned = df_cleaned.sort_values('frp', ascending=False)\
        .drop_duplicates(subset=['lat_r', 'lon_r', 'time_bin'])\
        .drop(columns=['lat_r', 'lon_r', 'time_bin'])

    print(f"spatial deduplication step: {tmp_df_len - len(df_cleaned)} removed")

    print(f"\n \n Total rows removed {len(df) - len(df_cleaned)}")

    return df_cleaned

def categorize_frp(x):
    if x <= 5: # marginal
        return 0
    elif 5 < x <= 25: # small
        return 1
    elif 25 < x <= 100: # medium
        return 2
    elif 100 < x <= 500: # large
        return 3
    else: #extreme
        return 4

def compute_fire_geometry(df):
    # 1.d compute perimeter of fire and burnt area estimates
    geoms = (
        df[df['spatial_cluster'] >= 0]
        .groupby('event_id')
        .apply(compute_cluster_geometry)
        .rename('geometry')
        .reset_index()
    )

    gdf = gpd.GeoDataFrame(geoms, geometry='geometry', crs='EPSG:4326')
    gdf_proj = gdf.to_crs('EPSG:3310')
    gdf['perimeter_km'] = gdf_proj.geometry.length / 1000
    gdf['area_km2']= gdf_proj.geometry.area / 1e6

    return gdf

def cluster_fire_pixel(df):
    df = df.loc[df['isFire'] == 1]

    # 1.b  cluster data into spatial location and time --> gather into events
    # Pass 1 — spatial clustering on full year (eps ~5km)
    spatial = DBSCAN(eps=0.05, min_samples=3).fit(df[['latitude', 'longitude']])
    df['spatial_cluster'] = spatial.labels_

    # Pass 2 — within each spatial cluster, split by gaps > 5 days

    df['time_subgroup'] = (
        df[df['spatial_cluster'] >= 0]
        .groupby('spatial_cluster', group_keys=False)
        .apply(assign_time_subgroup)
    )

    # Combine into a single event ID
    df['event_id'] = (
        df['spatial_cluster'].astype(str) + '_' +
        df['time_subgroup'].astype(str)
    )


    df_cluster = (
        # if cluster are <=0, they are just one pixel -> remove them
        df[df['spatial_cluster'] >= 0]
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
    df_cluster['duration_days'] = ( 
        pd.to_datetime(df_cluster['last_seen']) - pd.to_datetime(df_cluster['first_seen'])
        ).dt.days + 1

    return df, df_cluster

def combine_aqi_metrics():
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
    df_aqi = df_all.loc[df_all['n_missing_values'] <= 9].reset_index() # keep rows where at least 2 metrics

    # step 2.4 : compute global AQI value based on max AQI_pollutant value
    df_aqi['max_AQI'] = df_aqi.apply(lambda row: get_max_AQI(row), axis =1 )

    df_aqi['Units_PM2.5'] = 'ug/m3 LC'
    df_aqi['Units_O3'] = 'ppm'
    df_aqi['Units_NO2'] = 'ppb'
    df_aqi['Units_CO'] = 'ppm'

    df_aqi = df_aqi.fillna('N/A')
    df_aqi['Date'] = pd.to_datetime(df_aqi['Date'])
    return df_aqi

def main(args):

    ### ------ step 1: fire preprocess ------ ###
    print("=" * 60)
    print("Starting Data Processing\n")
    print("=" * 60)

    df_fire = pd.read_csv(FIRE_RAW_PATH)
    if not args.skip_cleaning_fire_data:
        print("Cleaning original fire dataset\n")

        # preprocess columns + clean data
        df_fire['diff'] = df_fire['brightness'] - df_fire['bright_t31']
        df_fire['isFire'] = df_fire.apply(lambda row: is_fire(row), axis=1)
        df_fire['fire_cat'] = df_fire['frp'].apply(lambda x: categorize_frp(x))

        df_cleaned = clean_fire_data(df_fire)
        # df_cleaned.to_csv(FIRE_PIXEL_PATH)
        print("=" * 20)

    if not args.skip_fire:
        print("Creating fire events and geometry\n")

        df_clustered, df_events = cluster_fire_pixel(df_cleaned)
        gdf_geometry = compute_fire_geometry(df_clustered)
        
        # merge everything
        df_events = df_events.merge(gdf_geometry[['event_id', 'perimeter_km', 'area_km2', 'geometry']], on='event_id')
        # df_events.to_csv(FIRE_EVENTS_PATH)
        print("=" * 20)

    ## step 2: Air quality report aggregation
    if not args.skip_aqi:
        print("Aggregating Air Quality Metrics\n")

        df_aqi = combine_aqi_metrics()
        # df_aqi.to_csv(AIR_QUALITY_REPORT_PATH)
        print("=" * 20)
    print("=" * 60)
    print("Process Ended.")
    print("=" * 60)

def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--skip_cleaning_fire_data", action="store_true", help="Skip fire preprocess")
    p.add_argument("--skip_fire", action="store_true", help="Skip fire preprocess")
    p.add_argument("--skip_aqi",   action="store_true", help="Skip aqi preprocess")
    return p.parse_args()


if __name__ == "__main__":

    args = parse_args()
    
    main(args)
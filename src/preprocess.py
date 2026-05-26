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
     FIRE_RAW_PATH, FIRE_PIXEL_PATH, FIRE_PERIMETER,
     OZONE_PATH, NITROGEN_DIOXIDE_PATH, PM10_PATH, PM25_PATH,
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



def get_max_AQI(row):
    val_max = row[['Daily AQI Value_PM2.5', 'Daily AQI Value_O3', 'Daily AQI Value_NO2', 'Daily AQI Value_PM10']].max()
    return val_max


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


def combine_aqi_metrics():
    df_o3= pd.read_csv(OZONE_PATH)
    df_o3 = df_o3.drop(columns=AQI_DROP_COLUMNS, errors='ignore')

    df_pm25 = pd.read_csv(PM25_PATH)
    df_pm25 = df_pm25.drop(columns=AQI_DROP_COLUMNS, errors='ignore')

    df_no2 = pd.read_csv(NITROGEN_DIOXIDE_PATH)
    df_no2 = df_no2.drop(columns=AQI_DROP_COLUMNS, errors='ignore')


    df_co = pd.read_csv(PM10_PATH)
    df_co = df_co.drop(columns=AQI_DROP_COLUMNS, errors='ignore')


    # step 2.2 : merge data
    df_all = df_pm25.merge(df_o3, on=AQI_MERGE_COLUMNS, how='outer', suffixes=['_PM2.5', '_O3']
                            ).merge(df_no2, on=AQI_MERGE_COLUMNS, how='outer'
                            ).merge(df_co, on=AQI_MERGE_COLUMNS, how='outer', suffixes=['_NO2', '_PM10']
                            )

    # step 2.3 : compute and filter on missing values
    df_all['n_missing_values'] = df_all.apply(lambda row: row.isnull().sum(), axis=1)
    df_aqi = df_all.loc[df_all['n_missing_values'] <= 9].reset_index() # keep rows where at least 2 metrics

    # step 2.4 : compute global AQI value based on max AQI_pollutant value
    df_aqi['max_AQI'] = df_aqi.apply(lambda row: get_max_AQI(row), axis =1 )

    df_aqi['Units_PM2.5'] = 'ug/m3 LC'
    df_aqi['Units_O3'] = 'ppm'
    df_aqi['Units_NO2'] = 'ppb'
    df_aqi['Units_PM'] = 'ug/m3 SC'

    df_aqi = df_aqi.fillna('N/A')
    df_aqi['Date'] = pd.to_datetime(df_aqi['Date'])
    return df_aqi

def add_fire_name_stats(df, gdf_perimeter):

    gdf_fire = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs="EPSG:4326"
    )

    joined = gpd.sjoin(
        gdf_fire, 
        gdf_perimeter[['poly_IncidentName', 'poly_GISAcres', 'attr_FireCause', 'attr_POOState', 'attr_POOCounty', 'geometry']],
        how='left', 
        predicate='within'
    )

    # Points with no match → no named perimeter
    joined['in_named_fire'] = joined['poly_IncidentName'].notna()
    joined = joined.loc[ joined.in_named_fire == True]

    return joined

def main(args):

    ### ------ step 1: fire preprocess ------ ###
    print("=" * 60)
    print("Starting Data Processing\n")
    print("=" * 60)

    print("Loading datasets\n")
    df_fire = pd.read_csv(FIRE_RAW_PATH)
    gdf_fire_perimeter = gpd.read_file(FIRE_PERIMETER)

    gdf_fire_perimeter['discovery'] = pd.to_datetime(gdf_fire_perimeter['attr_FireDiscoveryDateTime'])
    gdf_fire_perimeter = gdf_fire_perimeter[gdf_fire_perimeter['discovery'].dt.year.isin([2025])]

    if not args.skip_cleaning_fire_data:
        print("Cleaning original fire dataset\n")

        # preprocess columns + clean data
        df_fire['diff'] = df_fire['brightness'] - df_fire['bright_t31']
        df_fire['isFire'] = df_fire.apply(lambda row: is_fire(row), axis=1)
        df_fire['fire_cat'] = df_fire['frp'].apply(lambda x: categorize_frp(x))
        df_fire.to_csv(FIRE_RAW_PATH)

        df_fire_perimeter = add_fire_name_stats(df_fire, gdf_fire_perimeter)

        df_cleaned = clean_fire_data(df_fire_perimeter)
        df_cleaned.to_csv(FIRE_PIXEL_PATH)
        print("=" * 20)


    ## step 2: Air quality report aggregation
    if not args.skip_aqi:
        print("Aggregating Air Quality Metrics\n")

        df_aqi = combine_aqi_metrics()
        df_aqi.to_csv(AIR_QUALITY_REPORT_PATH)
        print("=" * 20)
    print("=" * 60)
    print("Process Ended.")
    print("=" * 60)

def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--skip_cleaning_fire_data", action="store_true", help="Skip fire preprocess")
    p.add_argument("--skip_aqi",   action="store_true", help="Skip aqi preprocess")
    return p.parse_args()


if __name__ == "__main__":

    args = parse_args()
    
    main(args)
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
     OZONE_PATH, NITROGEN_DIOXIDE_PATH, PM10_PATH, PM25_PATH, AIR_QUALITY_REPORT_PATH,
     WIND_RAW_PATH, WIND_PROCESSED_PATH
)
    

AQI_COLS = ['Daily AQI Value_PM2.5', 'Daily AQI Value_O3', 'Daily AQI Value_NO2', 'Daily AQI Value_PM10']
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

MERGE_COLS = ['Site Num',
              'Latitude',
              'Longitude',
              'State Name',
              'County Name',
              'Local Site Name',
              'Date Local',
              ]

DROP_COLS = [   'State Code', 
                'County Code', 
                'Event Type', 
                'AQI',
                'Address', 
                'City Name', 
                'CBSA Name',
                'Date of Last Change'
                'Datum', 
                'Pollutant Standard',
                'Parameter Name',
                'Parameter Code',
                'POC',
                'Sample Duration',
                'Observation Count', 
                'Observation Percent']

# def get_max_AQI(row):
#     val_max = row[AQI_COLS].max()
#     return val_max


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
    # df_cleaned = df_cleaned.loc[df_cleaned['isFire'] == 1]
    # print(f"Fire filtering step: {len(df) - tmp_df_len} removed")
    # tmp_df_len = len(df_cleaned)

    # d. frp threshold
    # df_cleaned = df_cleaned.loc[df_cleaned['frp'] > min_fpr_thr]
    # print(f"FRP filtering step: {tmp_df_len - len(df_cleaned)} removed")
    # tmp_df_len = len(df_cleaned)
    
    # e. scan/track pixels threshold
    # df_cleaned = df_cleaned.loc[(df_cleaned['scan'] < max_px_thr) & (df_cleaned['track'] < max_px_thr)]
    # print(f"pixel size filtering step: {tmp_df_len - len(df_cleaned)} removed")
    # tmp_df_len = len(df_cleaned)

    # # f. spatial duplication
    # df_cleaned['acq_datetime'] = df_cleaned['acq_date'].astype(str).str.replace('-','')
    # df_cleaned['acq_datetime'] = df_cleaned['acq_datetime'] + df_cleaned['acq_time'].astype(str).str.zfill(4)
    # df_cleaned['acq_datetime'] = pd.to_datetime(df_cleaned['acq_datetime'], format='%Y%m%d%H%M')

    # df_cleaned['lat_r'] = df_cleaned['latitude'].round(3)   # ~111m per 0.001°
    # df_cleaned['lon_r'] = df_cleaned['longitude'].round(3)
    # df_cleaned['time_bin'] = df_cleaned['acq_datetime'].dt.floor('12h')

    # df_cleaned = df_cleaned.sort_values('frp', ascending=False)\
    #     .drop_duplicates(subset=['lat_r', 'lon_r', 'time_bin'])\
    #     .drop(columns=['lat_r', 'lon_r', 'time_bin'])

    # print(f"spatial deduplication step: {tmp_df_len - len(df_cleaned)} removed")

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
    # df_aqi = df_all.loc[df_all['n_missing_values'] <= 9].reset_index() # keep rows where at least 2 metrics

    # step 2.4 : compute global AQI value based on max AQI_pollutant value
    df_aqi = compute_scores(df_all, penalty_factor=0.2)
    
    df_aqi['Units_PM2.5'] = 'ug/m3 LC'
    df_aqi['Units_O3'] = 'ppm'
    df_aqi['Units_NO2'] = 'ppb'
    df_aqi['Units_PM'] = 'ug/m3 SC'

    df_aqi = df_aqi.fillna('N/A')
    df_aqi['Date'] = pd.to_datetime(df_aqi['Date'])
    return df_aqi

def compute_scores(df, penalty_factor=0.2):
    aqi = df.copy()

    aqi = aqi[AQI_COLS]
    exceedance = (aqi - 50).clip(lower=0)   # zero for AQI <= 50

    df["max_AQI"] = aqi.max(axis=1)

    # Compute exceedances, total, first, and secondary
    # EPA guidelenies return first exceedance
    # Secondary exceedance: sum of above-threshold exceedances for every
    # pollutant that is NOT the dominant one. 
    # AQI 30 contributes 0; one at AQI 80 contributes 30.
    dominant_exceedance  = (df["max_AQI"] - 50).clip(lower=0)
    total_exceedance     = exceedance.sum(axis=1, min_count=1)
    secondary_exceedance = (total_exceedance - dominant_exceedance).clip(lower=0)
 
    # 1. composite_sum -------------------------------------------------------
    # max_AQI (dominant pollutant, full raw value) + secondary exceedances.
    # Keeps the dominant pollutant on its natural AQI scale while adding only
    df["sum_AQI"] = df["max_AQI"] + secondary_exceedance
 
    # 2. composite_penalty ---------------------------------------------------
    # Conservative: anchors on max_AQI and adds a fractional uplift from
    # secondary exceedances only.
    # Formula: max_AQI + penalty_factor * secondary_exceedance
    df["composite_penalty"] = df["max_AQI"] + penalty_factor * secondary_exceedance
 
    # 3. hidden_pollution ----------------------------------------------------
    # Exceedance burden discarded by the EPA max method:
    # everything above-threshold in secondary pollutants that max_AQI ignores.
    df["hidden_pollution"] = secondary_exceedance
 
    # 4. n_pollutants --------------------------------------------------------
    df["n_pollutants"] = aqi.notna().sum(axis=1)

    return df


def add_fire_name_stats(df, gdf_perimeter):

    gdf_fire = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs="EPSG:4326"
    )

    joined = gpd.sjoin(gdf_fire, gdf_perimeter[['poly_IncidentName', 'poly_GISAcres',
                                            'attr_FireCause', 'attr_POOState','attr_FireOutDateTime',
                                            'attr_POOCounty', 'geometry', 'attr_FireDiscoveryDateTime', 
                                            'attr_ICS209RptForTimePeriodFrom', 'attr_ContainmentDateTime']],
                    how='left', predicate='within')

    # Points with no match → no named perimeter
    joined['in_named_fire'] = joined['poly_IncidentName'].notna()
    joined = joined.loc[ joined.in_named_fire == True]

    # Make sure types are compatible
    joined['acq_date'] = pd.to_datetime(joined['acq_date'])
    joined['attr_FireDiscoveryDateTime'] = pd.to_datetime(joined['attr_FireDiscoveryDateTime'])

    # gather all possible end dates
    # For example palisades event didn't have OutDateTime or Containment Date but attr_ICS209RptForTimePeriodFrom for some reason
    joined['attr_FireOutDateTime'] = pd.to_datetime(joined['attr_FireOutDateTime'])
    joined['attr_ICS209RptForTimePeriodFrom'] = pd.to_datetime(joined['attr_ICS209RptForTimePeriodFrom'])
    joined['attr_ContainmentDateTime'] = pd.to_datetime(joined['attr_ContainmentDateTime'])

    joined['endFire'] = joined.apply(lambda row:  row[['attr_FireOutDateTime', 'attr_ICS209RptForTimePeriodFrom', 'attr_ContainmentDateTime']].dropna().min() , axis=1)

    df_fire = joined[
        (joined['acq_date'] >= joined['attr_FireDiscoveryDateTime']) &
        (
            joined['attr_FireOutDateTime'].isna() |          # still active
            (joined['acq_date'] <= joined['endFire'])
        )
    ]

    df_fire[df_fire.columns[6:]]

    return df_fire

def process_wind_vectors(df_wind, scale = 0.01):
    
    df_wind_direction = df_wind.loc[df_wind['Parameter Name'] == 'Wind Direction - Resultant']
    df_wind_speed = df_wind.loc[df_wind['Parameter Name'] == 'Wind Speed - Resultant']

    df_wind_direction = df_wind_direction.drop(columns=DROP_COLS, errors='ignore')
    df_wind_speed = df_wind_speed.drop(columns=DROP_COLS, errors='ignore')

    merged = df_wind_direction.merge(
        df_wind_speed, 
        on=MERGE_COLS, 
        how='outer',
        suffixes=[' DIR', ' SPEED']
        )

    ## Compute additional lat and long to draw vector 
    merged['u'] = -merged['Arithmetic Mean SPEED'] * np.sin(np.radians(merged['Arithmetic Mean DIR']))  # east component
    merged['v'] = -merged['Arithmetic Mean SPEED'] * np.cos(np.radians(merged['Arithmetic Mean DIR']))  # north component

    merged['lat2'] = merged['Latitude']  + merged['v'] * scale
    merged['lon2'] = merged['Longitude'] + merged['u'] * scale

    ## Compute the two arrowheads:
    merged['dlat'] = merged['lat2'] - merged['Latitude']
    merged['dlon'] = merged['lon2'] - merged['Longitude']

    merged['theta'] = np.arctan2(merged['dlon'], merged['dlat'])                # arrow direction angle
    merged['wing_len'] = 0.3 * np.sqrt(merged['dlat']**2 + merged['dlon']**2)   # 30% of arrow length
    spread = np.radians(25)                                                     # wing opening angle

    merged['left_lat']  = merged['lat2'] + merged['wing_len'] * np.cos(merged['theta'] + np.pi + spread)
    merged['left_lon']  = merged['lon2'] + merged['wing_len'] * np.sin(merged['theta'] + np.pi + spread)
    merged['right_lat'] = merged['lat2'] + merged['wing_len'] * np.cos(merged['theta'] + np.pi - spread)
    merged['right_lon'] = merged['lon2'] + merged['wing_len'] * np.sin(merged['theta'] + np.pi - spread)

    return merged

def main(args):

    ### ------ step 1: fire preprocess ------ ###
    print("=" * 60)
    print("Starting Data Processing\n")
    print("=" * 60)

    print("Loading datasets\n")
    df_fire = pd.read_csv(FIRE_RAW_PATH)
    gdf_fire_perimeter = gpd.read_file(FIRE_PERIMETER)
    df_wind = pd.read_csv(WIND_RAW_PATH)

    gdf_fire_perimeter['discovery'] = pd.to_datetime(gdf_fire_perimeter['attr_FireDiscoveryDateTime'])
    gdf_fire_perimeter = gdf_fire_perimeter[gdf_fire_perimeter['discovery'].dt.year.isin([2025])]

    if not args.skip_fire:
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


    ## step 3: Wind vector computstion
    if not args.skip_wind:
        print("Computing Wind components\n")
        df_wind = df_wind.loc[df_wind['State Name'] == 'California']

        df_processed_wind = process_wind_vectors(df_wind)

        df_processed_wind.to_csv(WIND_PROCESSED_PATH)
        print("=" * 20)

    print("=" * 60)
    print("Process Ended.")
    print("=" * 60)

def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--skip_fire", action="store_true", help="Skip fire preprocess")
    p.add_argument("--skip_aqi",   action="store_true", help="Skip aqi preprocess")
    p.add_argument("--skip_wind",   action="store_true", help="Skip wind preprocess")
    return p.parse_args()


if __name__ == "__main__":

    args = parse_args()
    
    main(args)
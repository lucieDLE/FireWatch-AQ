from pathlib import Path

ROOT = Path(__file__).parent.parent

AREA_LON = (-125.0, -113.0)
AREA_LAT = (32.0, 43.0)
SELECTED_DAY = '2025-09-08'


# Raw data
FIRE_RAW_PATH = ROOT / 'data/raw/fire_archive_J1V-C2_749152.csv'
FIRE_PERIMETER = ROOT / 'data/raw/WFIGS_Interagency_Perimeters_-8730464049412665158.geojson'
WIND_RAW_PATH =  ROOT / 'data/raw/daily_WIND_2025.csv'
ANNUAL_CONCENTRATION_PATH = ROOT / 'data/raw/annual_conc_by_monitor_2025.csv'

OZONE_PATH = ROOT / 'data/raw/ad_viz_plotval_data-O3.csv'
PM25_PATH = ROOT / 'data/raw/ad_viz_plotval_data-pm25.csv'
PM10_PATH = ROOT / 'data/raw/ad_viz_plotval_data-pm10.csv'
NITROGEN_DIOXIDE_PATH = ROOT / 'data/raw/ad_viz_plotval_data-NO2.csv'
# CARBON_MONOXIDE_PATH = ROOT / 'data/raw/ad_viz_plotval_data-CO.csv'


# Processed data (output of preprocess.py)
FIRE_EVENTS_PATH           = ROOT / 'data/processed/fire_event_2025.csv'
FIRE_PIXEL_PATH            = ROOT / 'data/processed/fire_archive_pixels_2025_cleaned.csv'
AIR_QUALITY_REPORT_PATH    = ROOT / 'data/processed/input_report_2025.csv'
WIND_PROCESSED_PATH        = ROOT / 'data/processed/wind_california_2025.csv' 

EVENT_START      = '2025-08-24'
EVENT_END        = '2025-09-18'
BASELINE_START   = '2025-08-10'
BASELINE_END     = '2025-08-16'

FIRE_LAT= (36.6, 37.2)
FIRE_LON = (-119.2, -118.9)

CENTER_LAT = 37.37
CENTER_LON =-120.54


POLLUTANT_THRESHOLDS = {
    "Ozone": [0.070, 'ppm'],
    "PM2.5 - Local Conditions": [35, 'ug/m3'] ,
    "PM10 Total 0-10um STP":[150, 'ug/m3'],
    "Nitrogen dioxide (NO2)": [100, 'ppb'],
    "Sulfur dioxide": [75, 'ppb'],
    "Carbon monoxide": [9, 'ppm'],
}

POLLUTANT_STANDARD_NAMES = ['Ozone 8-hour 2015', 'PM25 24-hour 2024', 'PM10 24-hour 2006', 'SO2 1-hour 2010','NO2 1-hour 2010', 'CO 8-hour 1971']
POLLUTANT_SAMPLE_DURATION = ['8-HR RUN AVG BEGIN HOUR', '24-HR BLK AVG', '1 HOUR', '8-HR RUN AVG END HOUR']
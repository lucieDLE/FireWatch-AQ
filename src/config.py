from pathlib import Path

ROOT = Path(__file__).parent.parent

AREA_LON = (-125.0, -113.0)
AREA_LAT = (32.0, 43.0)

CENTER_LAT = sum(AREA_LAT) / 2
CENTER_LON = sum(AREA_LON) / 2

# Raw data
FIRE_RAW_PATH = ROOT / 'data/fire_archive_J1V-C2_749152.csv'

OZONE_PATH = ROOT / 'data/raw/ad_viz_plotval_data-O3.csv'
PM25_PATH = ROOT / 'data/raw/ad_viz_plotval_data-pm25.csv'
NITROGEN_DIOXIDE_PATH = ROOT / 'data/raw/ad_viz_plotval_data-NO2.csv'
CARBON_MONOXIDE_PATH = ROOT / 'data/raw/ad_viz_plotval_data-CO.csv'


# Processed data (output of preprocess.py)
FIRE_EVENTS_PATH           = ROOT / 'data/fire_event_2025.csv'
FIRE_EVENTS_GDF_PATH       = ROOT / 'data/fire_event_2025_gdf.geojson'
AIR_QUALITY_REPORT_PATH    = ROOT / 'data/processed/input_report_2025.csv'

# Palisades Fire study
LA_FIRE_CENTROID = (34.07, -118.55)   
EVENT_START      = '2025-01-07'
EVENT_END        = '2025-01-12'
BASELINE_START   = '2025-01-01'       # 6 days before fire = clean baseline
BASELINE_END     = '2025-01-06'


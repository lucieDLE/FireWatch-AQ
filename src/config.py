from pathlib import Path

ROOT = Path(__file__).parent.parent

AREA_LON = (-125.0, -113.0)
AREA_LAT = (32.0, 43.0)

CENTER_LAT = sum(AREA_LAT) / 2
CENTER_LON = sum(AREA_LON) / 2

# Raw data
FIRE_RAW_PATH = ROOT / 'data/raw/fire_archive_J1V-C2_749152.csv'

OZONE_PATH = ROOT / 'data/raw/ad_viz_plotval_data-O3.csv'
PM25_PATH = ROOT / 'data/raw/ad_viz_plotval_data-pm25.csv'
NITROGEN_DIOXIDE_PATH = ROOT / 'data/raw/ad_viz_plotval_data-NO2.csv'
CARBON_MONOXIDE_PATH = ROOT / 'data/raw/ad_viz_plotval_data-CO.csv'


# Processed data (output of preprocess.py)
FIRE_EVENTS_PATH           = ROOT / 'data/processed/fire_event_2025.csv'
AIR_QUALITY_REPORT_PATH    = ROOT / 'data/processed/input_report_2025.csv'

EVENT_START      = '2025-08-24'
EVENT_END        = '2025-09-18'
BASELINE_START   = '2025-08-10'
BASELINE_END     = '2025-08-16'


from pathlib import Path

ROOT = Path(__file__).parent.parent

AREA_LON = (-125.0, -113.0)
AREA_LAT = (32.0, 43.0)

CENTER_LAT = sum(AREA_LAT) / 2
CENTER_LON = sum(AREA_LON) / 2

# Raw data
FIRE_RAW_PATH              = ROOT / 'data/fire_archive_J1V-C2_749152.csv'

# Processed data (output of preprocess.py)
FIRE_EVENTS_PATH           = ROOT / 'data/fire_event_2025.csv'
FIRE_EVENTS_GDF_PATH       = ROOT / 'data/fire_event_2025_gdf.geojson'

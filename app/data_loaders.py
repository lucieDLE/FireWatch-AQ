from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import json
import urllib.request
import pandas as pd

from src.config import AIR_QUALITY_REPORT_PATH, FIRE_PIXEL_PATH, ANNUAL_CONCENTRATION_PATH

df_aqi = pd.read_csv(AIR_QUALITY_REPORT_PATH)
df_fire = pd.read_csv(FIRE_PIXEL_PATH)
df_aqr_annual = pd.read_csv(ANNUAL_CONCENTRATION_PATH)

with urllib.request.urlopen(
    "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/california-counties.geojson"
) as f:
    ca_geojson = json.load(f)

import path_setup  # noqa: F401

import json
import urllib.request
import pandas as pd

from src.config import (
    AIR_QUALITY_REPORT_PATH, FIRE_PIXEL_PATH, ANNUAL_CONCENTRATION_PATH,
    CA_COUNTIES_GEOJSON_URL, CA_COUNTIES_GEOJSON_PATH,
)

df_aqi = pd.read_csv(AIR_QUALITY_REPORT_PATH)
df_fire = pd.read_csv(FIRE_PIXEL_PATH)
df_aqr_annual = pd.read_csv(ANNUAL_CONCENTRATION_PATH)


def _load_ca_geojson():
    if CA_COUNTIES_GEOJSON_PATH.exists():
        with open(CA_COUNTIES_GEOJSON_PATH) as f:
            return json.load(f)
    with urllib.request.urlopen(CA_COUNTIES_GEOJSON_URL) as f:
        data = json.load(f)
    with open(CA_COUNTIES_GEOJSON_PATH, 'w') as f:
        json.dump(data, f)
    return data

ca_geojson = _load_ca_geojson()

import path_setup  # noqa: F401

import json
import urllib.request
import pandas as pd
import geopandas as gpd
from shapely.geometry import box

from src.config import (
    AIR_QUALITY_REPORT_PATH, FIRE_PIXEL_PATH, ANNUAL_CONCENTRATION_PATH,
    CA_COUNTIES_GEOJSON_URL, CA_COUNTIES_GEOJSON_PATH,
    US_TOP_CITIES, SATELLITE_BOUNDS_PATH, SATELLITE_URL_PREFIX,
)

df_aqi = pd.read_csv(AIR_QUALITY_REPORT_PATH)
df_fire = pd.read_csv(FIRE_PIXEL_PATH)
df_aqr_annual = pd.read_csv(ANNUAL_CONCENTRATION_PATH)


def load_ca_geojson():
    if CA_COUNTIES_GEOJSON_PATH.exists():
        with open(CA_COUNTIES_GEOJSON_PATH) as f:
            return json.load(f)
    with urllib.request.urlopen(CA_COUNTIES_GEOJSON_URL) as f:
        data = json.load(f)
    with open(CA_COUNTIES_GEOJSON_PATH, 'w') as f:
        json.dump(data, f)
    return data

ca_geojson = load_ca_geojson()

def load_cities():
    df_us_cities = pd.read_csv(US_TOP_CITIES)
    gdf_us_cities = gpd.GeoDataFrame(
        df_us_cities, geometry=gpd.points_from_xy(df_us_cities.lon, df_us_cities.lat), crs="EPSG:4326"
    )
    return gdf_us_cities

ca_cities = load_cities()


def load_satellite_bounds():
    with open(SATELLITE_BOUNDS_PATH) as f:
        raw = json.load(f)
    return {name.split('snapshot-')[1].split('T')[0]: (name, bounds)
            for name, bounds in raw.items()}

satellite_bounds = load_satellite_bounds()
ALL_SATELLITE_DATES = sorted(satellite_bounds)


def list_available_satellite_dates():
    return ALL_SATELLITE_DATES


def satellite_dates_in_range(start_date, end_date):
    return [d for d in ALL_SATELLITE_DATES if start_date <= d <= end_date]


satellite_cache: dict = {}

def get_satellite_layer(date_str):
    if date_str in satellite_cache:
        return satellite_cache[date_str]

    if date_str not in satellite_bounds:
        return None

    filename, (min_x, min_y, max_x, max_y) = satellite_bounds[date_str]

    # image layer corners: top-left, top-right, bottom-right, bottom-left
    corners = [
        [min_x, max_y], [max_x, max_y],
        [max_x, min_y], [min_x, min_y],
    ]

    bbox_geometry = box(min_x, min_y, max_x, max_y)
    gpd_polygon_area = gpd.GeoDataFrame(geometry=[bbox_geometry], crs="EPSG:4326")
    gdf_cities_in_frame = ca_cities.sjoin(gpd_polygon_area, predicate='within')

    source = f'{SATELLITE_URL_PREFIX}/{filename}'

    result = ({'source': source, 'coordinates': corners}, gdf_cities_in_frame)
    satellite_cache[date_str] = result
    return result

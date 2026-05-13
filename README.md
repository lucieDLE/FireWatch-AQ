# FireWatch-AQ
Fire and Smoke Air Quality Assessment

## Project Overview

An interactive geospatial platform focused on a single wildfire event (Southern California), combining satellite fire detection data with ground-level air quality readings. Users explore fire hotspots on a map, click monitoring stations, and view detailed pollutant reports showing how a fire degrades air quality across a region.

**Target event:** 2025, Los Angeles County
**Why:** Dense AQ monitoring network, major fire events



## Data Sources 

- Air quality and metrics:
https://aqs.epa.gov/aqsweb/airdata/download_files.html

by year/county --> select all sites in CA

- Fires
https://firms.modaps.eosdis.nasa.gov/download/list.php



| Column Name  | Value   | Meaning |
|--------------|---------|--------------|
| `brightness` | 295.12 | Temperature in Kelvin. |
| `bright_t31` | 276.88 | Temperature in Kelvin. This measures the "background" temperature of the land surface. The difference between `brightness` and `bright_t31` is actually what the algorithm uses to detect fires  |
| `confidence` | `n`, `l`, `h` | low, nominal, and high. Detection reliability n and h are good.|
| `frp` | 0.65 | Fire radiative power in megawatts |
| `daynight` | `D` or `N` | Daytime or Nighttime. Nighttime detections are often more reliable since no solar reflection |
| `type` | 0, 2 or 3 | Inferred hot spot type: 0-> vegetation fire, 1-> volcano, 2-> other static land source, ->3 offshore. Filter only on 0. |


sources: https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs

# FireWatch-AQ
Fire and Smoke Air Quality Assessment

## Project Overview

An interactive geospatial platform focused on a single wildfire event (Southern California), combining satellite fire detection data with ground-level air quality readings. 
The project goal is to understand how wildfire smoke degrades air quality — specifically: how far smoke travels (spatial) and how long AQ
takes to recover (temporal).

**Target event:** Palisades Fire in January of 2025, Los Angeles County
**Why:** Dense AQ monitoring network, major fire events

Note: LA as a major city, has a worse AQI than other areas. To really evaluate impact, should either pick another region or take this into account



## Data Sources 

- Air quality and metrics:
https://aqs.epa.gov/aqsweb/airdata/download_files.html

by year/county --> select all sites in CA


Each CSV file contains the AQI for that specific pollutant only. The AQI scale has different breakpoints and formulas for each pollutant, so the same "raw" conditions produce different AQI numbers depending on which pollutant you're calculating it for. For example, on the same day at the same monitor:



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


https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf

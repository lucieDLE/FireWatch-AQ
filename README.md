# FireWatch-AQ: Fire & Smoke Air Quality Assessment

An interactive geospatial platform that examines how wildfire smoke degrades air quality, combining satellite fire detection data with ground-level air quality readings around a single wildfire event in Southern California.

The project addresses two core questions:
- **Spatial:** How far does wildfire smoke travel from the ignition zone?
- **Temporal:** How long does it take for air quality to recover after a fire?

**Target events:** Major Southern California fire sites — including Gifford, Madre, and Garnet — selected for their dense air quality monitoring network and the severity of recent fire activity.

---

## Data Sources

### A. Air Quality (EPA AQS)

Both air quality datasets are sourced from the [U.S. Environmental Protection Agency (EPA) Air Quality System (AQS)](https://aqs.epa.gov/aqsweb/airdata/FileFormats.html), which aggregates measurements from ground-based monitoring stations across the United States and its territories.

#### A.1 — Annual Summary Data

**File:** `annual_conc_by_monitor_2025.csv`  
**Source:** [EPA AQS Download Portal](https://aqs.epa.gov/aqsweb/airdata/download_files.html)

Each physical monitor appears in multiple rows because (a) the same measurement is evaluated against several historical regulatory standards, and (b) the same raw hourly data is aggregated at different time windows (1-hour, 3-hour, 24-hour). After filtering to the current active regulatory standard per pollutant, the working dataset reduces to **3,743 monitor records across 6 pollutants**:

| Pollutant | Standard retained | Sample duration |
|-----------|-------------------|-----------------|
| Ozone | Ozone 8-hour 2015 | 8-HR RUN AVG BEGIN HOUR |
| PM2.5 | PM25 24-hour 2024 | 24-HR BLK AVG |
| PM10 | PM10 24-hour 2006 | 24-HR BLK AVG |
| NO2 | NO2 1-hour 2010 | 1 HOUR |
| SO2 | SO2 1-hour 2010 | 1 HOUR |
| CO | CO 8-hour 1971 | 8-HR RUN AVG END HOUR |

#### A.2 — Daily Data

**Source:** [EPA Outdoor Air Quality Data — Download Daily Data](https://www.epa.gov/outdoor-air-quality-data/download-daily-data)

Daily records are downloaded by year and county, selecting all California monitoring sites for 2025. All files are then aggregated into a single CSV where each monitor has a value (potentially empty) for each pollutant. A **Max AQI** column is computed as the maximum AQI observed across all pollutants for a given day and location.

> To Download the data: select California, one pollutant, and all sites.

---

### B. Fire Detections (NASA FIRMS / VIIRS)

Fire detections are sourced from [NASA's FIRMS (Fire Information for Resource Management System)](https://firms.modaps.eosdis.nasa.gov/download/), using the **VIIRS instrument aboard the NOAA-20 (N20) satellite** at 375 m spatial resolution. The dataset spans approximately one year of observations from late 2024 through early 2026, with a primary focus on 2025.

> Downloading requires registering your email on the [FIRMS download portal](https://firms.modaps.eosdis.nasa.gov/download/). A full description of all data columns is available in the [FIRMS Active Fire Data Attributes reference](https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs).

#### Derived Columns

Two fields are computed prior to analysis:

| Column | Description |
|--------|-------------|
| `diff` | `brightness − bright_t31`: the difference between the VIIRS I4 mid-infrared band (~3.74 µm) and the I5 longwave infrared band (~11.45 µm). This isolates the thermal anomaly caused by active combustion — i.e., a thermal contrast index. |
| `isFire` | Binary fire confirmation flag, derived from `diff` using day/night-specific thresholds (see below). |

#### `isFire` Threshold Logic

The `isFire` flag is computed following the methodology described in [NASA's fire detection training materials (slides 9–10)](https://appliedsciences.nasa.gov/sites/default/files/2023-03/D1P5_FireDetection_Final.pdf). Daytime detections require a higher threshold (25 K vs. 10 K at night) because solar heating raises background surface temperatures, compressing the thermal contrast signal.

```
isFire = (daynight == 'D' AND diff > 25) OR (daynight == 'N' AND diff > 10)
```

#### Data Cleaning Steps

The raw dataset is filtered through the following steps in order:

1. **Confidence filter** — retain only `High` and `Nominal` confidence detections.
2. **Fire type filter** — retain vegetation fires only (`type == 0`).
3. **Thermal contrast filter** — retain only detections where `isFire == 1`, removing false positives that passed the confidence and type filters but lack sufficient thermal anomaly.
4. **FRP filter** — retain only detections with `frp >= 5 MW`. The FRP distribution is heavily right-skewed with a large concentration of detections below 5 MW, which correspond to marginal or near-noise fire signals.

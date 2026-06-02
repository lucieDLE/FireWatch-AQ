# FireWatch-AQ

## Tech Stack

| Role | Tool | 
|------|------|
| Dashboard framework | **Dash** |
| Maps | **Plotly Mapbox**  |
| Charts | **Plotly**  |
| Data wrangling | **pandas, geopandas** |
| API calls | **requests** |
| Geo utilities | **shapely** (distance rings, fire perimeter) |
| Styling | **CSS** (Dash supports custom stylesheets) |


## Phase 1 — Setup & Data Ingestion
*Notebooks: data exploration and API testing*

### Step 1: Environment & Project Structure (TODO)

```
firewatch-aq/
├── notebooks/
├── data/
├── src/
│   ├── data_processing.py
│   ├── figures.py
│   └── config.py
├── app/
│   ├── app.py
│   ├── layout.py
│   ├── callbacks.py
│   └── assets/
│       └── style.css
├── .env
├── requirements.txt
└── README.md
```

## Phase 2 — Fire Map & Station Visualization

### Idea: Distance Rings & Wind

- wind move smoke in specific direction -> differents monitors can react
- Wind direction arrow as an annotation or custom marker 
- Optional: smoke plume polygon projected downwind

---


### Step 15: Documentation & Deployment
- Screenshots and demo GIF for portfolio/sharing

---

## Phase 6 — (Ideas for Future Work)

### Step 16: Health Impact Layer
- Population density overlay
- Vulnerable facilities as additional map markers
- Exposure metric: AQI × population × duration


### Step 18: Historical Comparison
- Compare Palisades Fire against past LA fires
- Multi-year AQ trend analysis
- Seasonal baselines stored as zarr datasets

---

## Development Plan

```
Step 1              [x]Environment setup, install Dash + Plotly
Step 2              [x] Download and clean data
Step 3              [x] Explore data in notebooks
Step 4              [x] Fire hotspot map in Plotly (notebook)
Step 5              [x] Add AQ stations to the map (notebook)
Step 7              [x] Pollutant bar chart function (notebook)
Step 8              [x] Time series trend chart (notebook)
Step 9              [x] AQI (notebook)
Step 10             [x] Assemble Dash app shell
Step 11             [x] Wire up map click / report callback
Step 12             [x] Add controls (date slider, dropdowns)
Step 6 (optional)   [ ] Distance rings + wind overlay
Step 13             [x] Dark theme + CSS polish
Step 14             [ ] Metric cards + summary bar
Step 15             [ ] Docs + deploy
```

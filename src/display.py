WATCH_SITES =  { 
    
    'Las Palisades':[ 
        60374009, # Long Beach
        60374008, # Signal Beach (LBSH)
        60371302, # Compton
        60371103, # L.A.
        60370113, # West L.A.
    ],
    
    'Eaton': [
        60372005, # Pasadena
    ],


    'Garnet - Site 1': [
        60190011, #Fresno - Garland
        60190007, #Fresno-Drummond
        60190242, #Fresno-Sky Park
        60190500, #Table Mountain Air Monitoring Site
        60192016, #Fresno-Foundry
        60194001, #Parlier
        60195001, #Clovis-Villa

    ],

    'Garnet - Site 2': [
        60270002, #WMRC/NCORE
        60271023, #Bishop Tribe EMO
        60271033, #Stn.1 Big Pine Paiute site
        60271003, #Keeler
        60271018, #Lone Pine Paiute-Shoshone Reservation

    ]
}

AQI_CMAP = [ 
    [0, 'green'],         # [0-50]
    [0.125, 'yellow'],    # [51-100]
    [0.25, 'orange'],     # [101-150]
    [0.5, 'red'],         # [151-200]
    [0.75, 'purple'],     # [201-300]
    [1.0, 'maroon']       # [301-400]
]

COLORS_MAP = {
                'SIERRA': [
                    "rgb(120,155,185)",   # steel blue
                    "rgb(72,105,140)",    # slate blue
                    "rgb(170,195,215)",   # pale blue
                    "rgb(90,125,155)",    # muted blue
                    "rgb(50,80,115)",     # deep navy
                ],

                'FRESNO': [
                    "rgb(34,120,50)",     # forest green
                    "rgb(80,170,80)",     # mid green
                    "rgb(140,195,90)",    # light green
                    "rgb(20,80,35)",      # deep green
                    "rgb(100,150,60)",    # olive green
                    "rgb(170,210,120)",   # pale green
                    "rgb(55,130,65)",     # sage green
                ],

                # Fire perimeter traces
                'FIRE': [
                    "rgba(244,140,6,1.0)",   # amber — burning area
                    "rgba(201,68,0,1.0)",    # flame — perimeter
                ],
            }


AQI_BANDS_COLOR = [
    (0,   50,  'rgba(0, 228, 0, 0.15)'),      # Good
    (51,  100, 'rgba(255, 255, 0, 0.20)'),    # Moderate
    (101, 150, 'rgba(255, 126, 0, 0.15)'),    # Unhealthy for Sensitive
    (151, 200, 'rgba(255, 0, 0, 0.15)'),      # Unhealthy
    (201, 300, 'rgba(143, 63, 151, 0.15)'),   # Very Unhealthy
    (301, 400, 'rgba(143, 63, 151, 0.15)'),   # Hazardous
]

AQI_HOVER_TEMPLATE = (
    '<b>Air Quality Report at %{customdata[15]}</b><br>'
    '─────────────────<br>'
    'Date: %{customdata[0]}<br>'
    'Site Number: %{customdata[14]}<br><br>'
    '<b>Global AQI Value: %{customdata[1]}</b><br>'
    '<b>PM2.5:</b> %{customdata[2]} %{customdata[3]} [AQI: %{customdata[4]}]<br>'
    '<b>PM 10:</b> %{customdata[11]} %{customdata[12]} [AQI: %{customdata[13]}]<br>'
    '<b>Ozone (O3):</b> %{customdata[5]} %{customdata[6]} [AQI: %{customdata[7]}]<br>'
    '<b>Nitrogen Dioxide (NO2):</b> %{customdata[8]} %{customdata[9]} [AQI: %{customdata[10]}]<br>'
    '<extra></extra>'
)


AQI_REPORT_COLS = [
    'Date', 'max_AQI',
    'Daily Mean PM2.5 Concentration', 'Units_PM2.5', 'Daily AQI Value_PM2.5',
    'Daily Mean PM10 Concentration', 'Units_PM10', 'Daily AQI Value_PM10',
    'Daily Max 8-hour Ozone Concentration', 'Units_O3', 'Daily AQI Value_O3',
    'Daily Max 1-hour NO2 Concentration', 'Units_NO2', 'Daily AQI Value_NO2',
    'Site ID', 'Local Site Name'
]

FIRE_REPORT_COLS = [
    'acq_date', 'perimeter_km', 'area_km2', 'max_frp'
]

FIRE_HOVER_TEMPLATE = (
    '<b> FIRE STATS on %{customdata[0]}</b><br>'
    '─────────────────<br>'
    '<b>Perimeter: %{customdata[1]} km</b><br>'
    '<b>Estimated burnt area :</b> %{customdata[2]} km2<br>'
    '<b>Max FRP :</b> %{customdata[3]} MW<br>'
    '<extra></extra>'
)

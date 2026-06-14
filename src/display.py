MARGIN=dict(l=10, r=10, t=100, b=80)
TITLE_DICT= dict(font=dict(size=15),xanchor='center', x=0.5)

LEGEND_BOTTOM = dict(
    orientation='h',
     yanchor='top', xanchor='center', x=0.5,
    font=dict(size=11),
)
STATE_NAME_TO_CODE = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY', 'District Of Columbia': 'DC',
    'Puerto Rico': 'PR', 'Virgin Islands': 'VI',
}

WATCH_SITES =  {
    #TODO: investigates the two sites that fail
    'San Luis Obispo/Santa Barbara': [
        60798002,
        60792020,
        60792007,
        60792004,
        # 60793109,
        60831009,
        60832004,
    ],
    
    'Los Angeles': [
        60372005, # Pasadena
        60374009, # Long Beach
        60374008, # Signal Beach (LBSH)
        60371103, # L.A.
        60370113, # West L.A.
        60371302,
        60371201,
        60374010,
        60370016,
        # 60371027,
    ],

    'Fresno': [
        60190011, #Fresno - Garland
        60190007, #Fresno-Drummond
        60190242, #Fresno-Sky Park
        60190500, #Table Mountain Air Monitoring Site
        60192016, #Fresno-Foundry
        60194001, #Parlier
        60195001, #Clovis-Villa

    ],

    'Sierra National Forest': [
        60270002, #WMRC/NCORE
        60271023, #Bishop Tribe EMO
        60271033, #Stn.1 Big Pine Paiute site
        60271003, #Keeler
        60271018, #Lone Pine Paiute-Shoshone Reservation

    ]
}

FIRE_WATCH_SITES={
    'Gifford': ['San Luis Obispo/Santa Barbara',"Los Angeles" ],
    'Madre': ['San Luis Obispo/Santa Barbara', "Los Angeles"],
    'Garnet':['Fresno', 'Sierra National Forest'],
    'PALISADES':['Los Angeles', 'San Luis Obispo/Santa Barbara']
}


green_colors = [
    "rgba(199, 233, 192,0.8)",  # #c7e9c0
    "rgba(161, 217, 155,0.8)",  # #a1d99b
    "rgba(116, 196, 118,0.8)",  # #74c476
    "rgba(65, 171, 93,0.8)",    # #41ab5d
    "rgba(35, 139, 69,0.8)",    # #238b45
    "rgba(0, 90, 50,0.8)",      # #005a32
]

line_greens = [
    "rgba(161, 217, 155,1.0)",  # #a1d99b
    "rgba(116, 196, 118,1.0)",  # #74c476
    "rgba(65, 171, 93,1.0)",    # #41ab5d
    "rgba(35, 139, 69,1.0)",    # #238b45
    "rgba(0, 90, 50,1.0)",      # #005a32
    "rgba(0, 68, 27,1.0)",      # #00441b
]

line_reds = [
    'rgba(250,140,85,1.0)',
    'rgba(250,140,85,1.0)',
    'rgba(250,100,70,1.0)',
    'rgba(227,74,51,1.0)',
    'rgba(179,0,0,1.0)',
    'rgba(100,0,0,1.0)'
    ]

red_colors = [
    'rgba(254,240,217,0.8)',
    'rgba(253,204,138,0.8)',
    'rgba(253,187,132,0.8)',
    'rgba(252,141,89,0.8)',
    'rgba(227,74,51,0.8)',
    'rgba(179,0,0,0.8)', 
    ]


FIRE_CAT_NAMES = ["Very Small", "Small", "Medium", "Large", "Extreme"]
FIRE_CAT_ = [
    "Very Small: (≤5 MW)",
    "Small: (5-25 MW)",
    "Medium: (25-100 MW)",
    "Large: (100-500 MW)",
    "Extreme: (>500 MW)",
  ]


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
                    "rgb(185,220,245)",   # icy pale blue
                    "rgb(140,190,225)",   # powder blue
                    "rgb(100,160,210)",   # cornflower blue
                    "rgb(65,125,185)",    # medium blue
                    "rgb(40,95,160)",     # strong blue
                    "rgb(20,60,125)",     # deep navy
                    "rgb(75,145,175)",    # teal blue
                    "rgb(115,155,195)",   # steel periwinkle
                    "rgb(50,110,150)",    # ocean blue
                ],

                'FRESNO': [
                    "rgb(195,235,155)",   # pale spring green
                    "rgb(150,210,110)",   # light fresh green
                    "rgb(100,180,75)",    # bright mid green
                    "rgb(60,150,50)",     # medium forest green
                    "rgb(25,115,35)",     # rich forest green
                    "rgb(10,75,25)",      # deep forest green
                    "rgb(125,170,65)",    # olive green
                    "rgb(170,215,105)",   # light olive green
                    "rgb(55,130,85)",     # sage green
                ],

                # Fire perimeter traces
                'FIRE': [
                    "rgba(244,140,6,1.0)",   # amber — burning area
                    "rgba(201,68,0,1.0)",    # flame — perimeter
                ],
            }


AQI_BANDS_COLOR = [
    (0,   50,  'rgba(0, 228, 0, 0.30)'),      # Good
    (51,  100, 'rgba(255, 255, 0, 0.35)'),    # Moderate
    (101, 150, 'rgba(255, 126, 0, 0.30)'),    # Unhealthy for Sensitive
    (151, 200, 'rgba(255, 0, 0, 0.30)'),      # Unhealthy
    (201, 300, 'rgba(143, 63, 151, 0.30)'),   # Very Unhealthy
    (301, 400, 'rgba(143, 63, 151, 0.30)'),   # Hazardous
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

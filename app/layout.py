from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.display import COLORS_MAP

from data_transforms import *
from figures_aq import make_pollutant_distribution, make_aq_us_plot, compute_max_boxplot
from figures_fire import make_cloropleth_fire_counties, make_bar_fire_event, make_fire_aqi_overlay
from figures_event import make_aq_time_series, make_burning_area_plot, make_overlay_aq_fire


annual_pollutant_distribution = make_pollutant_distribution(df_aqr_annual)
pollutant_exceedances_us_map = make_aq_us_plot(df_county_aqr_annual, list_best=['WA', 'ID', 'MS'], list_worst=['CA', 'TX', 'AZ'])
pollutant_distribution_us_barplot = compute_max_boxplot(df_annual_stats, state_list)

top_counties = make_cloropleth_fire_counties(df_fire, ca_geojson)
top_fires = make_bar_fire_event(df_biggest_fire)
overlay_fire_aqi = make_fire_aqi_overlay(df_aq_quantile, df_biggest_fire)

# timeseries plots
ts_site_1 = make_aq_time_series(df_event_site_1, site_1, site_name=site_name_1, colors=COLORS_MAP['FRESNO'])
ts_site_2 = make_aq_time_series(df_event_site_2, site_2, site_name=site_name_2, colors=COLORS_MAP['SIERRA'])
burning_area = make_burning_area_plot(gdf, event_start=EVENT_START, event_end=EVENT_END)
aq_fire_overlay = make_overlay_aq_fire(
    df_day_site_1, df_day_site_2, gdf_fire_day, geojson_fire_dict,
    selected_day=SELECTED_DAY,
    site_name_1=site_name_1, site_name_2=site_name_2,
    center_lat=(FIRE_LAT[0] + FIRE_LAT[1]) / 2,
    center_lon=(FIRE_LON[0] + FIRE_LON[1]) / 2,
)


# ============================================================================
#  APP FUNCTIONS/ VARIABLES
# ============================================================================
def graphCard(fig_id, figure, height='400px'):
    return html.Div(
        dcc.Graph(id=fig_id, figure=figure, style={'height': height}),
        className="chart-card"
    )


def textCard(title="TITLE", text='some text'):
    return html.Div(
        dbc.Card([
            dbc.CardHeader(title),
            dbc.CardBody(dcc.Markdown(text)),
        ]),
    )

# ============================================================================
#  APP LAYOUT
# ============================================================================


def build_layout():

    dark_mode_switch =  html.Span([
            dbc.Label(className="fa fa-sun", html_for="switch"),
            dbc.Switch(id="switch-theme", value=True, className="d-inline-block ms-1", persistence=True),
            dbc.Label(className="fa fa-moon", html_for="switch"),
        ])

    layout = dbc.Container( fluid=True,
                                id="page-wrapper",
                                children=[ 
                                    html.Div([
                                        html.H4("FireWatch — Air Quality Assessment"),
                                        dark_mode_switch,
                                    ],className='app-header'
                                    ),
                                    dcc.Tabs([
                                        dcc.Tab(    
                                            label='Air Quality Data Exploration',
                                            children=[
                                                # ── Top row: 2 charts side by side ──────────────────
                                                dbc.Row([
                                                    dbc.Col(
                                                        graphCard("annual-pollutant-graph", annual_pollutant_distribution, height='420px'),
                                                        width=5
                                                    ),
                                                    dbc.Col(
                                                        graphCard("pollutant-exceedances-graph", pollutant_exceedances_us_map, height='420px'),
                                                        width=5
                                                    ),
                                                    dbc.Col(
                                                        textCard("Overview", "Add your analysis here."),
                                                        width=2
                                                    ),
                                                ]),
                                                # ── Bottom row: 1 full-width chart ──────────────────
                                                dbc.Row([
                                                    dbc.Col(
                                                        graphCard("pollutant-distribution-graph", pollutant_distribution_us_barplot, height='500px'),
                                                        width=12
                                                    ),
                                                ]),
                                                dbc.Row([
                                                    dbc.Col(
                                                        textCard("Key Findings", "Add your analysis here."),
                                                        width=12
                                                    ),
                                                ]),

                                            ]),

                                        dcc.Tab(
                                            label='Fire Data Exploration', 
                                            children=[ 
                                                dbc.Row([
                                                    dbc.Col(
                                                        graphCard("top-counties-graph", top_counties, height='420px'),
                                                        width=5
                                                    ),
                                                    dbc.Col(
                                                        graphCard("top-fire-graph", top_fires, height='420px'),
                                                        width=5
                                                    ),
                                                    dbc.Col(
                                                        textCard("Overview", "Add your analysis here."),
                                                        width=2
                                                    ),

                                                ]),
                                                # ── Bottom row: pollutant selector + overlay chart ──
                                                dbc.Row([
                                                    #Left Col
                                                    dbc.Col([
                                                        graphCard("overlay-fire-aqi-graph", overlay_fire_aqi, height='500px'),
                                                    ], width=10),
                                                    
                                                    # Right Col
                                                    dbc.Col([
                                                        dbc.Row([
                                                            dbc.Col([
                                                                textCard("Overview", "Select on Pollutant to visualize its impact on public Health and if it has a relationship with fire onset."),
                                                                dcc.Dropdown(
                                                                    id='pollutant-dropdown',
                                                                    options=[{'label': name, 'value': name} for name in POLLUTANT_COL_MAP],
                                                                    value='PM2.5',
                                                                    clearable=False,
                                                                ),
                                                                ]),
                                                        ], className='mb-2 mt-3 ms-2'),
                                                    ], width=2),
                                                ]),
                                                dbc.Row([
                                                    dbc.Col(
                                                        textCard("Key Findings", "Add your analysis here."),
                                                        width=12
                                                    ),
                                                ]),
                                            ]),

                                        # dcc.Tab(
                                        #     label='California Spike Insight', 
                                        #     children=[ html.Div('coming soon') ]),

                                        dcc.Tab(
                                            label='Event Time Series Visualization',
                                            children=[
                                                dbc.Row([
                                                    dbc.Col([
                                                        html.Label("Select Fire Event:", className="fw-bold mt-2"),
                                                        dcc.Dropdown(
                                                            id='fire-dropdown',
                                                            options=[{'label': name, 'value': name} for name in FIRE_OPTIONS],
                                                            value=DEFAULT_FIRE,
                                                            clearable=False,
                                                        ),
                                                    ], width=4, className='mb-3 mt-2'),
                                                ]),
                                                dbc.Row([
                                                    # left panel
                                                    dbc.Col([
                                                        textCard("Tab Description", "description Text"),
                                                        graphCard(fig_id="overlay-map-graph", figure=aq_fire_overlay, height='480px'),
                                                        html.Div(
                                                            dcc.Slider(
                                                                id='date-slider',
                                                                min=0,
                                                                max=len(event_dates) - 1,
                                                                step=1,
                                                                value=event_dates.index(SELECTED_DAY) if SELECTED_DAY in event_dates else 0,
                                                                marks={
                                                                    i: {'label': event_dates[i][5:],
                                                                        'style': {'fontSize': '11px'}}
                                                                    for i in range(0, len(event_dates), 3)
                                                                },
                                                                included=False,
                                                            ),
                                                            className='slider-container',
                                                        ),
                                                        graphCard(fig_id="burning-graph", figure=burning_area, height='320px'),
                                                    ]),
                                                    
                                                    # right panel
                                                    dbc.Col([
                                                        graphCard(fig_id="ts-site1-graph", figure=ts_site_1, height='400px'),
                                                        graphCard(fig_id="ts-site2-graph", figure=ts_site_2, height='400px'),
                                                        textCard("Tab Analysis", "analysis text"),
                                                    ])
                                                ])
                                            ]),
                                        ]),

                                    ],
                                )


    return layout
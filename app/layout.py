from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.config import *
from src.display import *
from figures import *
from data import *

# AQR qnnual
annual_pollutant_distribution = make_pollutant_distribution(df_aqr_annual)
pollutant_exceedances_us_map = make_aq_us_plot(df_county_aqr_annual, list_best = ['WA', 'ID', 'MS'], list_worst=['CA', 'TX', 'AZ'])
pollutant_distribution_us_barplot = compute_max_boxplot(df_annual_stats, state_list)

top_counties = make_cloropleth_fire_counties(df_fire)
top_fires = make_bar_fire_event(df_biggest_fire)
overlay_fire_aqi = make_fire_aqi_overlay(df_aq_quantile, df_biggest_fire)

# timeseries plots
ts_site_1= make_aq_time_series(df_event_site_1, site_1, 'Fresno Area', colors=COLORS_MAP['FRESNO'])
ts_site_2 = make_aq_time_series(df_event_site_2, site_2, 'Sierra National Forest - EAST', colors=COLORS_MAP['SIERRA'])
burning_area = make_burning_area_plot(gdf)
aq_fire_overlay = make_overlay_aq_fire(df_day_site_1, df_day_site_2, gdf_fire_day, geojson_fire_dict,)


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
                                                        width=10
                                                    ),
                                                    dbc.Col(
                                                        textCard("Key Findings", "Add your analysis here."),
                                                        width=2
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
                                                # ── Bottom row: 1 full-width chart ──────────────────
                                                dbc.Row([
                                                    dbc.Col(
                                                        graphCard("overlay-fire-aqi-graph", overlay_fire_aqi, height='500px'),
                                                        width=10
                                                    ),
                                                    dbc.Col(
                                                        textCard("Key Findings", "Add your analysis here."),
                                                        width=2
                                                    ),
                                                ]),
                                            ]),


                                        dcc.Tab(
                                            label='California Spike Insight', 
                                            children=[ html.Div('coming soon') ]),

                                        dcc.Tab(
                                            label='Event Time Serie Visualization',
                                            children=[
                                                dbc.Row([
                                                    # left panel
                                                    dbc.Col([
                                                        textCard("Tab Description", "description Text"),
                                                        graphCard(fig_id="overlay-map-graph", figure=aq_fire_overlay, height='480px'), 
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
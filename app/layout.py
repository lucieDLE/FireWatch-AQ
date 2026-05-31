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
import analysis

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
    df_day_site_1, df_day_site_2, gdf_fire_day, geojson_fire_dict, gdf_burnt_area, geojson_burnt_dict,
    selected_day=SELECTED_DAY,
    site_name_1=site_name_1, site_name_2=site_name_2,
    center_lat=map_center_lat, center_lon=map_center_lon,
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
                                                        textCard("Overview", analysis.PANEL_AIR_OVERVIEW),
                                                ]),
                                                dbc.Row([
                                                    dbc.Col(
                                                        graphCard("annual-pollutant-graph", annual_pollutant_distribution, height='420px'),
                                                        width=9,
                                                    ),
                                                    dbc.Col([
                                                        textCard(analysis.PANEL_AIR_CARD_MONITORS_1[0], analysis.PANEL_AIR_CARD_MONITORS_1[1]),
                                                        textCard(analysis.PANEL_AIR_CARD_MONITORS_2[0], analysis.PANEL_AIR_CARD_MONITORS_2[1]),
                                                    ], width=3,),
                                                ]),
                                                dbc.Row([

                                                    dbc.Col(
                                                        graphCard("pollutant-exceedances-graph", pollutant_exceedances_us_map, height='420px'),
                                                        width=9
                                                    ),
                                                    dbc.Col(
                                                        textCard(analysis.PANEL_AIR_CARD_MAP[0], analysis.PANEL_AIR_CARD_MAP[1]),
                                                        width=3,
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
                                                        textCard(analysis.PANEL_AIR_CARD_BOXPLOT_1[0], analysis.PANEL_AIR_CARD_BOXPLOT_1[1]),
                                                        width=4
                                                    ),
                                                    dbc.Col(
                                                        textCard(analysis.PANEL_AIR_CARD_BOXPLOT_2[0], analysis.PANEL_AIR_CARD_BOXPLOT_2[1]),
                                                        width=4
                                                    ),
                                                    dbc.Col(
                                                        textCard(analysis.PANEL_AIR_CARD_NOTE[0], analysis.PANEL_AIR_CARD_NOTE[1]),
                                                        width=4
                                                    ),
                                                ]),

                                            ]),

                                        dcc.Tab(
                                            label='Fire Data Exploration', 
                                            children=[ 

                                                dbc.Row([
                                                    dbc.Col(
                                                        textCard("Overview", analysis.PANEL_FIRE_OVERVIEW),
                                                    ),
                                                ]),
                                                dbc.Row([
                                                    dbc.Col(
                                                        graphCard("top-counties-graph", top_counties, height='420px'),
                                                        width=9
                                                    ),
                                                    dbc.Col(
                                                        textCard(analysis.PANEL_FIRE_CARD_COUNTY[0], analysis.PANEL_FIRE_CARD_COUNTY[1]),
                                                        width=3,
                                                    )
                                                ]),
                                                dbc.Row([
                                                    dbc.Col(
                                                        graphCard("top-fire-graph", top_fires, height='420px'),
                                                        width=9
                                                    ),
                                                    dbc.Col(
                                                        textCard(analysis.PANEL_FIRE_CARD_TOP10[0], analysis.PANEL_FIRE_CARD_TOP10[1]),
                                                        width=3,
                                                    )
                                                ]),
                                                # ── Bottom row: pollutant selector + overlay chart ──
                                                dbc.Row([
                                                    #Left Col
                                                    dbc.Col([
                                                        graphCard("overlay-fire-aqi-graph", overlay_fire_aqi, height='500px'),
                                                    ], width=9),
                                                    
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
                                                                textCard(analysis.PANEL_FIRE_BOXPLOT_PM25[0], analysis.PANEL_FIRE_BOXPLOT_PM25[1])
                                                        ], className='mb-2 mt-3 ms-2'),
                                                    ], width=3),
                                                ]),
                                            ]),

                                        dcc.Tab(
                                            label='Event Time Series Visualization',
                                            children=[
                                                dbc.Row([
                                                    dbc.Col([
                                                        html.Div(
                                                            dbc.Card([
                                                                dbc.CardHeader("TAB DESCRIPTION"),
                                                                dbc.CardBody([
                                                                    dcc.Markdown(analysis.PANEL_EVENT_OVERVIEW_PREAMBLE),
                                                                    dbc.Row([
                                                                        dbc.Col(dcc.Markdown(analysis.PANEL_EVENT_OVERVIEW_FIRES), width=6),
                                                                        dbc.Col(dcc.Markdown(analysis.PANEL_EVENT_OVERVIEW_ABBREVIATIONS), width=6),
                                                                    ]),
                                                                ]),
                                                            ])
                                                        ),
                                                    ])
                                                ]),
                                                dbc.Row([
                                                    # left panel
                                                    dbc.Col([
                                                        html.Label("Select Fire Event:", className="fw-bold mt-2"),
                                                        dcc.Dropdown(
                                                            id='fire-dropdown',
                                                            options=[{'label': name, 'value': name} for name in FIRE_OPTIONS],
                                                            value=DEFAULT_FIRE,
                                                            clearable=False,
                                                        ),
                                                        textCard(analysis.PANEL_EVENT_MADRE_DESCRIPTION[0], analysis.PANEL_EVENT_MADRE_DESCRIPTION[1]),

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
                                                                included=True,
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
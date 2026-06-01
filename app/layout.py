from pathlib import Path
import sys
import re
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


def bodyCard(text):
    return html.Div(
        dbc.Card([
            dbc.CardBody(dcc.Markdown(text)),
        ]),
    )


def _fmt_refs(text):
    """Convert [N](url) → superscript link and [N-M] standalone → superscript."""
    text = re.sub(
        r'\[(\d+)\]\((https?://[^)]+)\)',
        r'<sup><a href="\2" target="_blank">[\1]</a></sup>',
        text
    )
    text = re.sub(r'\[(\d+-\d+)\](?!\()', r'<sup>[\1]</sup>', text)
    return text


def introMd(text):
    return dcc.Markdown(_fmt_refs(text), dangerously_allow_html=True)


def introTextCard(title, text):
    return html.Div(dbc.Card([
        dbc.CardHeader(title),
        dbc.CardBody(introMd(text)),
    ], className="intro-card"))


def hookCard(icon_class, text):
    return html.Div([
        html.Div([
            html.I(className=f"fa {icon_class}"),
        ], className="hook-badge"),
        dbc.Card(dbc.CardBody(introMd(text)), className="intro-card"),
    ], className="hook-card-wrapper")


def introBodyCard(text):
    return html.Div(dbc.Card([
        dbc.CardBody(introMd(text)),
    ], className="intro-card"))


def sectionTitle(text, align='left'):
    return html.Div(
        html.H5(text, className="section-title"),
        style={"textAlign": align}
    )


def aqi_table():
    rows = [
        ("0–50",   "Good",                           "#00E400", "#000",  "Air quality is satisfactory; little or no risk."),
        ("51–100",  "Moderate",                       "#FFFF00", "#000",  "Acceptable; some people may experience symptoms for some pollutants."),
        ("101–150", "Unhealthy for Sensitive Groups", "#FF7E00", "#000",  "Members of sensitive groups may experience health effects."),
        ("151–200", "Unhealthy",                      "#FF0000", "#fff",  "Everyone may begin to experience health effects."),
        ("201–300", "Very Unhealthy",                 "#8F3F97", "#fff",  "Health warnings of emergency conditions. Entire population is more likely to be affected."),
        ("301–500", "Hazardous",                      "#7E0023", "#fff",  "Health alert: everyone may experience serious health effects."),
    ]
    return html.Div(
        html.Table([
            html.Thead(html.Tr([
                html.Th("AQI", style={"width": "60px"}),
                html.Th("Category"),
                html.Th("Health Concern"),
            ], className="aqi-table-head")),
            html.Tbody([
                html.Tr([
                    html.Td(aqi, style={"background": color, "color": text_color, "fontWeight": "700",
                                        "textAlign": "center", "padding": "6px 8px", "borderRadius": "4px",
                                        "whiteSpace": "nowrap"}),
                    html.Td(cat, style={"background": color, "color": text_color, "fontWeight": "600",
                                        "padding": "6px 10px"}),
                    html.Td(health, style={"padding": "6px 10px", "fontSize": "0.85rem"}),
                ])
                for aqi, cat, color, text_color, health in rows
            ])
        ], className="aqi-table"),
        className="aqi-table-wrapper"
    )


def naaqs_table():
    # color: None=neutral, 'red'=NAAQS more lenient than WHO, 'green'=NAAQS stricter
    rows = [
        ("SO₂",   "1-hour",  "75 ppb",                 "—",            None),
        ("PM2.5", "24-hour", "35 µg/m³",               "15 µg/m³",     "red"),
        ("PM10",  "24-hour", "150 µg/m³",              "45 µg/m³",     "red"),
        ("Ozone", "8-hour",  "0.070 ppm → 137 µg/m³", "100 µg/m³",    "red"),
        ("NO₂",   "1-hour",  "100 ppb → 188 µg/m³",   "200 µg/m³",    "green"),
        ("CO",    "8-hour",  "9 ppm → 10,350 µg/m³",  "10,000 µg/m³", "red"),
    ]
    _color_style = {
        "red":   {"background": "rgba(220,50,50,0.12)", "color": "#b91c1c", "padding": "6px 12px"},
        "green": {"background": "rgba(22,163,74,0.12)", "color": "#15803d", "padding": "6px 12px"},
        None:    {"padding": "6px 12px"},
    }
    return html.Div(
        html.Table([
            html.Thead(html.Tr([
                html.Th("Pollutant"),
                html.Th("Averaging Time"),
                html.Th("NAAQS Threshold"),
                html.Th("WHO Guideline"),
            ], className="aqi-table-head")),
            html.Tbody([
                html.Tr([
                    html.Td(pol, style={"fontWeight": "600", "padding": "6px 12px"}),
                    html.Td(avg, style={"padding": "6px 12px", "color": "var(--md-on-surface-variant)"}),
                    html.Td(naaqs, style=_color_style[flag]),
                    html.Td(who,   style={"padding": "6px 12px"}),
                ])
                for pol, avg, naaqs, who, flag in rows
            ])
        ], className="aqi-table"),
        className="aqi-table-wrapper"
    )


def sources_card():
    sources_md = analysis.SOURCES_MD
    return dbc.Card([
        dbc.CardHeader("Sources"),
        dbc.CardBody(dcc.Markdown(sources_md)),
    ], className="sources-card intro-card")


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
                                            label='Introduction',
                                            children=[
                                                # ── Dashboard presentation ─────────────────────────
                                                dbc.Row([
                                                    dbc.Col(
                                                        html.Div(
                                                            dcc.Markdown(analysis.INTRO_DASHBOARD_PRESENTATION),
                                                            className="intro-presentation"
                                                        ),
                                                        width=12
                                                    ),
                                                ]),

                                                # ── Section 1: Three hooks ─────────────────────────
                                                dbc.Row([
                                                    dbc.Col(hookCard("fa-fire",      analysis.INTRO_SECTION_1_HOOK_1), width=3),
                                                    dbc.Col(hookCard("fa-chart-bar", analysis.INTRO_SECTION_1_HOOK_2), width=3),
                                                    dbc.Col(hookCard("fa-wind",      analysis.INTRO_SECTION_1_HOOK_3), width=3),
                                                ], className="justify-content-center", style={"marginTop": "60px"}),

                                                # ── Section 2: What is AQI? ────────────────────────
                                                dbc.Row([dbc.Col(sectionTitle("What is Air Quality Index (AQI)?", align='right'))]),
                                                dbc.Row([
                                                    dbc.Col(aqi_table(), width=6),
                                                    dbc.Col(introBodyCard(analysis.INTRO_SECTION_2_CARD_1), width=6),
                                                ], align="start"),

                                                # ── Section 3: Pollutants ──────────────────────────
                                                dbc.Row([dbc.Col(sectionTitle("Pollutants covered in this Dashboard", align='left'))]),
                                                dbc.Row([dbc.Col(introBodyCard(analysis.INTRO_SECTION_3_PM), width=5)]),
                                                dbc.Row([
                                                    dbc.Col(introTextCard(analysis.INTRO_SECTION_3_PM25[0], analysis.INTRO_SECTION_3_PM25[1]), width=4),
                                                    dbc.Col(introTextCard(analysis.INTRO_SECTION_3_PM10[0], analysis.INTRO_SECTION_3_PM10[1]), width=4),
                                                    dbc.Col(introTextCard(analysis.INTRO_SECTION_3_O3[0],   analysis.INTRO_SECTION_3_O3[1]),   width=4),
                                                ]),
                                                dbc.Row([
                                                    dbc.Col(introTextCard(analysis.INTRO_SECTION_3_NO2[0], analysis.INTRO_SECTION_3_NO2[1]), width=4),
                                                    dbc.Col(introTextCard(analysis.INTRO_SECTION_3_SO2[0], analysis.INTRO_SECTION_3_SO2[1]), width=4),
                                                    dbc.Col(introTextCard(analysis.INTRO_SECTION_3_CO[0],  analysis.INTRO_SECTION_3_CO[1]),  width=4),
                                                ]),

                                                # ── Section 4: NAAQS / WHO table ──────────────────
                                                dbc.Row([dbc.Col(sectionTitle("NAAQS Legal Thresholds and WHO Guidelines", align='right'))]),
                                                dbc.Row([
                                                    dbc.Col(naaqs_table(), width={"size": 8, "offset": 2}),
                                                ]),

                                                # ── Section 5: Why California? ─────────────────────
                                                dbc.Row([dbc.Col(sectionTitle("Why California?", align='left'))]),
                                                dbc.Row([
                                                    dbc.Col(introBodyCard(analysis.INTRO_SECTION_5_WHY[0]), width=5),
                                                ]),
                                                dbc.Row([
                                                    dbc.Col(introTextCard(analysis.INTRO_SECTION_5_FACTOR_1[0], analysis.INTRO_SECTION_5_FACTOR_1[1]), width=4),
                                                    dbc.Col(introTextCard(analysis.INTRO_SECTION_5_FACTOR_2[0], analysis.INTRO_SECTION_5_FACTOR_2[1]), width=4),
                                                    dbc.Col(introTextCard(analysis.INTRO_SECTION_5_FACTOR_3[0], analysis.INTRO_SECTION_5_FACTOR_3[1]), width=4),
                                                ]),

                                                # ── Sources ────────────────────────────────────────
                                                dbc.Row([dbc.Col(sources_card(), width=12)]),
                                            ]),

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
                                                ], align="start"),
                                                dbc.Row([
                                                    dbc.Col(
                                                        graphCard("pollutant-exceedances-graph", pollutant_exceedances_us_map, height='420px'),
                                                        width=9
                                                    ),
                                                    dbc.Col(
                                                        textCard(analysis.PANEL_AIR_CARD_MAP[0], analysis.PANEL_AIR_CARD_MAP[1]),
                                                        width=3,
                                                    ),
                                                ], align="start"),

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
                                                ], align="start"),
                                                dbc.Row([
                                                    dbc.Col(
                                                        graphCard("top-fire-graph", top_fires, height='420px'),
                                                        width=9
                                                    ),
                                                    dbc.Col(
                                                        textCard(analysis.PANEL_FIRE_CARD_TOP10[0], analysis.PANEL_FIRE_CARD_TOP10[1]),
                                                        width=3,
                                                    )
                                                ], align="start"),
                                                # ── Bottom row: pollutant selector + overlay chart ──
                                                dbc.Row([
                                                    #Left Col
                                                    dbc.Col([
                                                        graphCard("overlay-fire-aqi-graph", overlay_fire_aqi, height='500px'),
                                                    ], width=9),
                                                    
                                                    # Right Col
                                                    dbc.Col([
                                                        textCard("Overview", "Select a pollutant to visualize its impact on public health and its relationship with fire onset."),
                                                        dcc.Dropdown(
                                                            id='pollutant-dropdown',
                                                            options=[{'label': name, 'value': name} for name in POLLUTANT_COL_MAP if name != 'NO2'],
                                                            value='PM2.5',
                                                            clearable=False,
                                                            className='mb-3',
                                                        ),
                                                        dbc.Card([
                                                            dbc.CardHeader(id="pollutant-card-header", children=analysis.PANEL_FIRE_BOXPLOT_PM25[0]),
                                                            dbc.CardBody(dcc.Markdown(id="pollutant-card-body", children=analysis.PANEL_FIRE_BOXPLOT_PM25[1])),
                                                        ]),
                                                    ], width=3),
                                                ], align="start"),
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
                                                                    ], className="mb-0"),
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
                                                        dbc.Card([
                                                            dbc.CardHeader(id="event-desc-header", children=analysis.PANEL_EVENT_MADRE_DESCRIPTION[0]),
                                                            dbc.CardBody(dcc.Markdown(id="event-desc-body", children=analysis.PANEL_EVENT_MADRE_DESCRIPTION[1])),
                                                        ]),
                                                        graphCard(fig_id="burning-graph", figure=burning_area, height='300px'),
                                                    ],width=5),

                                                    dbc.Col([
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
                                                    ],width=7),
                                                ]),
                                                    
                                                dbc.Row([
                                                    dbc.Col([
                                                        graphCard(fig_id="ts-site1-graph", figure=ts_site_1, height='400px'),
                                                    ],width=6),
                                                    dbc.Col([
                                                        graphCard(fig_id="ts-site2-graph", figure=ts_site_2, height='400px'),
                                                    ],width=6),
                                                ]),
                                                dbc.Row([
                                                    dbc.Col([
                                                        dbc.Card([
                                                            dbc.CardHeader(id="event-site1-header", children=analysis.PANEL_EVENT_MADRE_ANALYSIS_SITE_1[0]),
                                                            dbc.CardBody(dcc.Markdown(id="event-site1-body", children=analysis.PANEL_EVENT_MADRE_ANALYSIS_SITE_1[1])),
                                                        ]),
                                                    ],width=6),
                                                    dbc.Col([
                                                        dbc.Card([
                                                            dbc.CardHeader(id="event-site2-header", children=analysis.PANEL_EVENT_MADRE_ANALYSIS_SITE_2[0]),
                                                            dbc.CardBody(dcc.Markdown(id="event-site2-body", children=analysis.PANEL_EVENT_MADRE_ANALYSIS_SITE_2[1])),
                                                        ]),
                                                    ],width=6),
                                                ])
                                            ]),
                                        ]),

                                    ],
                                )


    return layout
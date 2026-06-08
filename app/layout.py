import path_setup  # noqa: F401
import re

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.display import COLORS_MAP, red_colors, green_colors, line_greens, line_reds

from data_transforms import (
    # prepared dataframes / lookups
    df_aqi, df_fire, df_aqr_annual, df_county_aqr_annual, df_annual_stats,
    df_biggest_fire, df_aq_quantile, ca_geojson,
    state_list, list_best_codes, list_worst_codes, POLLUTANT_COL_MAP,
    misclassification_examples, get_fire_raw,
    # event panel (initial render for DEFAULT_FIRE)
    FIRE_OPTIONS, DEFAULT_FIRE, EVENT_START, EVENT_END, SELECTED_DAY, event_dates,
    site_1, site_2, site_name_1, site_name_2,
    df_event_site_1, df_event_site_2, df_day_site_1, df_day_site_2,
    gdf, gdf_fire_day, gdf_burnt_area, geojson_fire_dict, geojson_burnt_dict,
    map_center_lat, map_center_lon,
)
from figures_aq import make_pollutant_distribution, make_aq_us_plot, compute_max_boxplot
from figures_fire import make_cloropleth_fire_counties, make_bar_fire_event, make_fire_aqi_overlay
from figures_event import make_aq_time_series, make_burning_area_plot, make_overlay_aq_fire
from figures_explore import (
    make_scan_track_distribution, make_fire_data_entry_analysis, make_fire_category_repartition,
    make_barplot_sum_aqi, make_pollutant_number_pie_chart, make_wrong_guidance_plot,
)
import analysis


# ============================================================================
#  APP FUNCTIONS/ VARIABLES
# ============================================================================
def graph_card(fig_id, figure, height='400px'):
    return html.Div(
        dcc.Graph(id=fig_id, figure=figure, style={'height': height}),
        className="chart-card"
    )


def text_card(title="TITLE", text='some text', solid=False):
    # solid -> emphasized card (used for the orienting "Overview" blocks);
    # default -> lightened block that sits on the page background.
    if solid:
        return html.Div(
            dbc.Card([
                dbc.CardHeader(title),
                dbc.CardBody(dcc.Markdown(text)),
            ]),
        )
    return html.Div([
        html.Div(title, className="flat-block-title"),
        dcc.Markdown(text, className="flat-block-body"),
    ], className="flat-block")


def body_card(text):
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


def intro_mark_down(text):
    return dcc.Markdown(_fmt_refs(text), dangerously_allow_html=True)


def intro_text_card(title, text):
    return html.Div(dbc.Card([
        dbc.CardHeader(title),
        dbc.CardBody(intro_mark_down(text)),
    ], className="intro-card"))


def pollutant_card(symbol_children, source_icon, source_text, source_bg, title, desc, risk_level, risk_pct, color):
    return html.Div([
        html.Div([
            html.Div(symbol_children, className="poll-symbol", style={"color": color}),
            html.Div([
                html.I(className=f"fa {source_icon}", style={"marginRight": "5px"}),
                html.Span(source_text),
            ], className="poll-source-badge", style={"backgroundColor": source_bg}),
        ], className="poll-card-top"),
        html.P(html.Strong(title), className="poll-title"),
        dcc.Markdown(desc, className="poll-desc"),
        html.Div([
            html.Div([
                html.Span("Health risk", className="poll-risk-label"),
                html.Span(risk_level, className="poll-risk-value", style={"color": color}),
            ], className="poll-risk-row"),
            html.Div(
                html.Div(style={"width": f"{risk_pct}%", "height": "3px", "backgroundColor": color, "borderRadius": "2px"}),
                className="poll-risk-bar-bg"
            ),
        ], className="poll-risk-section"),
    ], className="poll-card")


def stat_card(stat_children, desc, bg_color):
    return html.Div([
        html.Div(stat_children, className="stat-top"),
        html.P(desc, className="stat-desc"),
    ], className="stat-card", style={"backgroundColor": bg_color})


# Pollutant-badge colors by AQI band, drawn from the project's red/green palettes.
# Good (≤50) → green; everything above scales up the red_colors ramp.
# (upper_bound, background, text color)
_AQI_BADGE_BANDS = [
    (50,  green_colors[2], line_greens[5]),  # good
    (100, red_colors[2],   line_reds[5]),    # moderate
    (150, red_colors[3],   line_reds[5]),    # unhealthy-SG
    (200, red_colors[4],   "var(--text)"),           # unhealthy
    (300, red_colors[5],   "var(--text)"),           # very unhealthy
    (500, red_colors[5],   "var(--text)"),           # hazardous
]


def aqi_badge_colors(value):
    for hi, bg, fg in _AQI_BADGE_BANDS:
        if value <= hi:
            return bg.replace('0.8', '0.6'), fg


def epa_report_card(value, category, text, bg_color):
    return html.Div([
            html.P("What the EPA reports", className="poll-group-label"),
            html.Span(str(value), className="stat-big"),
            html.P(category, className="stat-context"),
            dcc.Markdown(text, className="stat-desc"),
        ], className="stat-card", style={"backgroundColor": bg_color})

def pollutant_badge(p):
    """One poll: 'PM2.5 146', colored by AQI severity (grey if no reading)."""
    if p["value"] is None:
        return html.Span(f"{p['name']} —", className="misclass-badge misclass-badge-empty")
    bg, fg = aqi_badge_colors(p["value"])
    return html.Span(
        f"{p['name']} {p['value']}",
        className="misclass-badge",
        style={"backgroundColor": bg, "color": fg},
    )


def misclass_example_card(group):
    n = group["n_days"]
    title = f"{n} day{'s' if n != 1 else ''} misclassified as {group['epa_label']}"

    site_blocks = []
    for s in group["sites"]:
        site_blocks.append(html.Div([
            html.Div(f"{s['site']}, {s['county']}", className="misclass-site"),
            *[html.Div([pollutant_badge(p) for p in day], className="misclass-badges")
              for day in s["days"]],
        ], className="misclass-site-block"))
    
    epa_bg, epa_fg = aqi_badge_colors(group['epa_value'])
    sum_bg, sum_fg = aqi_badge_colors(group['sum_aqi_value'])


    return html.Div([
        html.Div(title, className="misclass-title"),
        html.Div([
            html.Span(
                f"EPA: {group['epa_label']} ({group['epa_value']})",
                className="misclass-poll misclass-poll-epa",
                style={"backgroundColor": epa_bg, "color": epa_fg},
                ),

            html.Span("→", className="misclass-arrow"),
            html.Span(
                f"sum AQI Exceedance: {group['sum_aqi_label']} ({group['sum_aqi_value']})",
                className="misclass-poll misclass-poll-composite",
                style={"backgroundColor": sum_bg, "color": sum_fg},
                ),

        ], className="misclass-polls"),
        *site_blocks,
    ], className="misclass-card")


def hook_card(icon_class, text):
    return html.Div([
        html.Div([
            html.I(className=f"fa {icon_class}"),
        ], className="hook-badge"),
        dbc.Card(dbc.CardBody(intro_mark_down(text)), className="intro-card"),
    ], className="hook-card-wrapper")


def intro_body_card(text):
    return html.Div(dbc.Card([
        dbc.CardBody(intro_mark_down(text)),
    ], className="intro-card"))


def section_title(text, align='left'):
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
#  TABS LAYOUT
# ============================================================================

def build_intro_tab():

    intro_tab =  dcc.Tab(
        label='Introduction',
        children=[
            # ── Hero ───────────────────────────────────────────
            html.Div([
                html.Div("2025 FIRE SEASON", className="hero-eyebrow"),
                html.H1("California.", className="hero-title"),
                html.P([
                    html.Span("8,036", className="hero-stat"), " fires.  ",
                    html.Span("525,223", className="hero-stat"), " acres burned.",
                ], className="hero-stats"),
                html.Hr(className="hero-divider"),
                html.P([
                    html.Em("This dashboard examines the air quality consequences of the 2025 California fire season: "),
                    html.Strong("tracing the link between fire activity and pollutant exposure across the state."),
                ], className="hero-desc"),
            ], className="hero-block"),

            # ── Section 1: Three hooks ─────────────────────────
            dbc.Row([
                dbc.Col(hook_card("fa-fire",      analysis.INTRO_SECTION_1_HOOK_1), width=3),
                dbc.Col(hook_card("fa-line-chart", analysis.INTRO_SECTION_1_HOOK_2), width=3),
                dbc.Col(hook_card("fa-wind",      analysis.INTRO_SECTION_1_HOOK_3), width=3),
            ], className="justify-content-center", style={"marginTop": "60px"}),

            # ── Section 2: What is AQI? ────────────────────────
            dbc.Row([dbc.Col(section_title("What is Air Quality Index (AQI)?", align='right'))]),
            dbc.Row([
                dbc.Col(aqi_table(), width=6),
                dbc.Col(intro_body_card(analysis.INTRO_SECTION_2_CARD_1), width=6),
            ], align="start"),


            # ── Section 4: NAAQS / WHO table ──────────────────
            dbc.Row([dbc.Col(section_title("Legal Thresholds and WHO Guidelines", align='left'))]),
            dbc.Row([
                dbc.Col(naaqs_table(), width=8),
            ]),
            dbc.Row([dbc.Col(section_title("Pollutants Covered in This Dashboard", align='right'))]),
            dbc.Row(
                className="justify-content-center g-4",
                children=[
                # ── Particulate Matter panel ───────────────────
                dbc.Col(html.Div([
                    html.Div("PARTICULATE MATTER", className="poll-group-label"),
                    dbc.Row([
                        dbc.Col(pollutant_card(
                            symbol_children=[html.Span("PM", className="poll-sym-text") ],
                            source_icon="fa-fire", source_text="various sources", source_bg="rgba(220,50,50,0.1)",
                            title="Particulate Matter",
                            desc=analysis.INTRO_SECTION_3_PM,
                            risk_level="Very high", risk_pct=90, color="var(--md-on-surface-variant)"
                        ),width=12),
                    ],className="mb-2"),
                    dbc.Row([

                        dbc.Col(pollutant_card(
                            symbol_children=[html.Span("PM", className="poll-sym-text"), html.Sub("2.5", className="poll-sym-sub")],
                            source_icon="fa-fire", source_text="Wildfires · combustion", source_bg="rgba(220,50,50,0.1)",
                            title="Fine particles",
                            desc=analysis.INTRO_SECTION_3_PM25,
                            risk_level="Very high", risk_pct=90, color="#5B5BD6"
                        ),width=6),
                        dbc.Col(pollutant_card(
                            symbol_children=[html.Span("PM", className="poll-sym-text"), html.Sub("10", className="poll-sym-sub")],
                            source_icon="fa-road", source_text="Dust · construction", source_bg="rgba(180,140,80,0.1)",
                            title="Coarse particles",
                            desc=analysis.INTRO_SECTION_3_PM10,
                            risk_level="Moderate", risk_pct=50, color="#8B7355"
                        ),width=6),
                    ],className="mb-2")
                ], className="poll-group-wrapper"), width=5),
                # ── Gaseous Pollutants panel ───────────────────
                dbc.Col(html.Div([
                    html.Div("GASEOUS POLLUTANTS", className="poll-group-label"),
                    dbc.Row([
                        dbc.Col(pollutant_card(
                            symbol_children=[html.Span("O", className="poll-sym-text"), html.Sub("3", className="poll-sym-sub")],
                            source_icon="fa-sun", source_text="Sunlight · smog", source_bg="rgba(220,50,50,0.1)",
                            title="Ground-level ozone",
                            desc=analysis.INTRO_SECTION_3_O3,
                            risk_level="Very high", risk_pct=90, color="#9B1C1C"
                        ), width=6),
                        dbc.Col(pollutant_card(
                            symbol_children=[html.Span("NO", className="poll-sym-text"), html.Sub("2", className="poll-sym-sub")],
                            source_icon="fa-bus", source_text="Transport · industry", source_bg="rgba(30,58,138,0.1)",
                            title="Nitrogen dioxide",
                            desc=analysis.INTRO_SECTION_3_NO2,
                            risk_level="High", risk_pct=70, color="#1E3A8A"
                        ), width=6),
                    ], className="mb-2"),
                    dbc.Row([
                        dbc.Col(pollutant_card(
                            symbol_children=[html.Span("CO", className="poll-sym-text")],
                            source_icon="fa-car", source_text="Motor vehicles", source_bg="rgba(55,65,81,0.1)",
                            title="Carbon monoxide",
                            desc=analysis.INTRO_SECTION_3_CO,
                            risk_level="Moderate", risk_pct=50, color="#374151"
                        ), width=6),
                        dbc.Col(pollutant_card(
                            symbol_children=[html.Span("SO", className="poll-sym-text"), html.Sub("2", className="poll-sym-sub")],
                            source_icon="fa-industry", source_text="Power · industry", source_bg="rgba(6,95,70,0.1)",
                            title="Sulfur dioxide",
                            desc=analysis.INTRO_SECTION_3_SO2,
                            risk_level="Moderate", risk_pct=50, color="#065F46"
                        ), width=6),
                    ],className="mb-2"),
                ], className="poll-group-wrapper"), width=5),
            ]),
            # ── Section 5: Why California? ─────────────────────
            dbc.Row([dbc.Col(section_title("Why California?", align='left'))]),

            dbc.Row(
                className="justify-content-center g-4",
                children=[
                dbc.Col(html.Div([
                    html.Div("Public Health Concerns", className="poll-group-label"),
                    dbc.Row([
                        dbc.Col(stat_card(
                            [html.Span("88%", className="stat-big")],
                            "Of Californians live in a community with unhealthy air",
                            "var(--stat-problem-1)"
                        ), width=6),
                        dbc.Col(stat_card(
                            [html.Span("5", className="stat-big"), html.Span(" of the ", className="stat-context"), html.Span("10", className="stat-big")],
                            "US cities most polluted are in California",
                            "var(--stat-problem-2)"
                        ), width=6),
                    ],className="g-4 mb-2"),
                    dbc.Row([
                        dbc.Col(stat_card(
                            [html.Span("26", className="stat-big"), html.Span(" of the ", className="stat-context"), html.Span("27", className="stat-big")],
                            "years Los Angeles has ranked as the most ozone-polluted city",
                            "var(--stat-problem-3)"
                        ), width=6),
                        dbc.Col(stat_card(
                            [html.Span("2", className="stat-big")],
                            "cities ranked 1st place in worst ozone and particle pollutions",
                            "var(--stat-problem-4)"
                        ), width=6),
                    ],className="g-4 mb-2",),
                ]),width=4),

                dbc.Col(html.Div([
                    html.Div("Signs of Progress", className="poll-group-label"),
                    dbc.Row([
                        dbc.Col(stat_card(
                            [html.Span("18.1", className="stat-big")],
                            "Fewer bad days for short-term particle pollution in Bakerfield",
                            "var(--stat-progress-1)"
                        ), width=6),
                        dbc.Col(stat_card(
                            [html.Span("#1", className="stat-big")],
                            "US state on zero-emission vehicle adoption",
                            "var(--stat-progress-2)"
                        ), width=6),
                    ],className="g-4 mb-2",),
                    dbc.Row([
                        dbc.Col(stat_card(
                            [html.Span("6", className="stat-big")],
                            "metro areas improved enough to leave the Worst 25 list",
                            "var(--stat-progress-3)"
                        ), width=6),
                        dbc.Col(stat_card(
                            [html.Span("18", className="stat-big"), html.Span(" of the ", className="stat-context"), html.Span("25", className="stat-big")],
                            "worst cities for daily PM2.5 improved vs. last year",
                            "var(--stat-progress-4)"
                        ), width=6),
                    ],className="g-4 mb-2"),
                ]),width=4),
            ]),
            dbc.Row([
                dbc.Col(html.Div("Causes and Risk Factors", className="poll-group-label", style={"textAlign": "center"})),
            ],),
            dbc.Row([
                dbc.Col(hook_card("fa-car", analysis.INTRO_SECTION_5_FACTOR_1), width=4),
                dbc.Col(hook_card("fa-thermometer-full", analysis.INTRO_SECTION_5_FACTOR_2), width=4),
                dbc.Col(hook_card("fa-globe", analysis.INTRO_SECTION_5_FACTOR_3), width=4),
            ]),

            # ── Sources ────────────────────────────────────────
            dbc.Row([dbc.Col(sources_card(), width=12)]),
        ])

    return intro_tab


def build_air_quality_tab():
    annual_pollutant_distribution = make_pollutant_distribution(df_aqr_annual)
    pollutant_exceedances_us_map = make_aq_us_plot(df_county_aqr_annual, list_best=list_best_codes, list_worst=list_worst_codes)
    pollutant_distribution_us_barplot = compute_max_boxplot(df_annual_stats, state_list)

    air_quality_tab = dcc.Tab(
        label='Air Quality Data Exploration',
        children=[
            # ── Top row: 2 charts side by side ──────────────────
            dbc.Row([
                    text_card("Overview", analysis.PANEL_AIR_OVERVIEW, solid=True),
            ]),
            dbc.Row([
                dbc.Col(
                    graph_card("annual-pollutant-graph", annual_pollutant_distribution, height='420px'),
                    width=9,
                ),
                dbc.Col([
                    text_card(analysis.PANEL_AIR_CARD_MONITORS_1[0], analysis.PANEL_AIR_CARD_MONITORS_1[1]),
                    text_card(analysis.PANEL_AIR_CARD_MONITORS_2[0], analysis.PANEL_AIR_CARD_MONITORS_2[1]),
                ], width=3,),
            ], align="start"),
            dbc.Row([
                dbc.Col(
                    graph_card("pollutant-exceedances-graph", pollutant_exceedances_us_map, height='420px'),
                    width=9
                ),
                dbc.Col(
                    text_card(analysis.PANEL_AIR_CARD_MAP[0], analysis.PANEL_AIR_CARD_MAP[1]),
                    width=3,
                ),
            ], align="start"),

            # ── Bottom row: 1 full-width chart ──────────────────
            dbc.Row([
                dbc.Col(
                    graph_card("pollutant-distribution-graph", pollutant_distribution_us_barplot, height='500px'),
                    width=12
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    text_card(analysis.PANEL_AIR_CARD_BOXPLOT_1[0], analysis.PANEL_AIR_CARD_BOXPLOT_1[1]),
                    width=4
                ),
                dbc.Col(
                    text_card(analysis.PANEL_AIR_CARD_BOXPLOT_2[0], analysis.PANEL_AIR_CARD_BOXPLOT_2[1]),
                    width=4
                ),
                dbc.Col(
                    text_card(analysis.PANEL_AIR_CARD_NOTE[0], analysis.PANEL_AIR_CARD_NOTE[1]),
                    width=4
                ),
            ]),

        ])
    return air_quality_tab


def build_fire_data_tab():
    top_counties = make_cloropleth_fire_counties(df_fire, ca_geojson)
    top_fires = make_bar_fire_event(df_biggest_fire)
    overlay_fire_aqi = make_fire_aqi_overlay(df_aq_quantile, df_biggest_fire)

    fire_data_tab = dcc.Tab(
        label='Fire Data Exploration', 
        children=[ 

            dbc.Row([
                dbc.Col(
                    text_card("Overview", analysis.PANEL_FIRE_OVERVIEW, solid=True),
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    graph_card("top-counties-graph", top_counties, height='420px'),
                    width=9
                ),
                dbc.Col(
                    text_card(analysis.PANEL_FIRE_CARD_COUNTY[0], analysis.PANEL_FIRE_CARD_COUNTY[1]),
                    width=3,
                )
            ], align="start"),
            dbc.Row([
                dbc.Col(
                    graph_card("top-fire-graph", top_fires, height='420px'),
                    width=9
                ),
                dbc.Col(
                    text_card(analysis.PANEL_FIRE_CARD_TOP10[0], analysis.PANEL_FIRE_CARD_TOP10[1]),
                    width=3,
                )
            ], align="start"),
            # ── Bottom row: pollutant selector + overlay chart ──
            dbc.Row([
                #Left Col
                dbc.Col([
                    graph_card("overlay-fire-aqi-graph", overlay_fire_aqi, height='500px'),
                ], width=9),
                
                # Right Col
                dbc.Col([
                    text_card("Overview", "Select a pollutant to visualize its impact on public health and its relationship with fire onset.", solid=True),
                    dcc.Dropdown(
                        id='pollutant-dropdown',
                        options=[{'label': name, 'value': name} for name in POLLUTANT_COL_MAP if name != 'NO2'],
                        value='PM2.5',
                        clearable=False,
                        className='mb-3',
                    ),
                    html.Div([
                        html.Div(id="pollutant-card-header", children=analysis.PANEL_FIRE_BOXPLOT_PM25[0], className="flat-block-title"),
                        dcc.Markdown(id="pollutant-card-body", children=analysis.PANEL_FIRE_BOXPLOT_PM25[1], className="flat-block-body"),
                    ], className="flat-block"),
                ], width=3),
            ], align="start"),
        ])
    return fire_data_tab


def build_time_serie_event():
    ts_site_1 = make_aq_time_series(df_event_site_1, site_1, site_name=site_name_1, colors=COLORS_MAP['FRESNO'])
    ts_site_2 = make_aq_time_series(df_event_site_2, site_2, site_name=site_name_2, colors=COLORS_MAP['SIERRA'])
    burning_area = make_burning_area_plot(gdf, event_start=EVENT_START, event_end=EVENT_END)
    aq_fire_overlay = make_overlay_aq_fire(
        df_day_site_1, df_day_site_2, gdf_fire_day, geojson_fire_dict, gdf_burnt_area, geojson_burnt_dict,
        selected_day=SELECTED_DAY,
        site_name_1=site_name_1, site_name_2=site_name_2,
        center_lat=map_center_lat, center_lon=map_center_lon,
    )

    time_serie_event = dcc.Tab(
    label='Event Time Series Visualization',
    children=[
        dbc.Row([
            dbc.Col([
                html.Div(
                    dbc.Card([
                        dbc.CardHeader("Overview"),
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
                graph_card(fig_id="burning-graph", figure=burning_area, height='300px'),
            ],width=5),

            dbc.Col([
                graph_card(fig_id="overlay-map-graph", figure=aq_fire_overlay, height='480px'),
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
                graph_card(fig_id="ts-site1-graph", figure=ts_site_1, height='400px'),
            ],width=6),
            dbc.Col([
                graph_card(fig_id="ts-site2-graph", figure=ts_site_2, height='400px'),
            ],width=6),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div(id="event-site1-header", children=analysis.PANEL_EVENT_MADRE_ANALYSIS_SITE_1[0], className="flat-block-title"),
                    dcc.Markdown(id="event-site1-body", children=analysis.PANEL_EVENT_MADRE_ANALYSIS_SITE_1[1], className="flat-block-body"),
                ], className="flat-block"),
            ],width=6),
            dbc.Col([
                html.Div([
                    html.Div(id="event-site2-header", children=analysis.PANEL_EVENT_MADRE_ANALYSIS_SITE_2[0], className="flat-block-title"),
                    dcc.Markdown(id="event-site2-body", children=analysis.PANEL_EVENT_MADRE_ANALYSIS_SITE_2[1], className="flat-block-body"),
                ], className="flat-block"),
            ],width=6),
        ])
    ])
    return time_serie_event


def build_behind_data():
    df_fire_raw = get_fire_raw()
    explore_sum_aqi      = make_barplot_sum_aqi(df_aqi)
    explore_pie          = make_pollutant_number_pie_chart(df_aqi)
    explore_wrong_guide  = make_wrong_guidance_plot(df_aqi)
    explore_scan_track   = make_scan_track_distribution(df_fire_raw)
    explore_data_entries = make_fire_data_entry_analysis(df_fire_raw)
    explore_category     = make_fire_category_repartition(df_fire_raw, df_fire)

    behind_data_tab = dcc.Tab(
    label='Behind the Data',
    value='behind-the-data',
    children=[
        dbc.Row([
            dbc.Col(
                text_card("Overview", analysis.PANEL_EXPLORE_OVERVIEW, solid=True),
            ),
        ]),
        # ══ Section 1: Rethinking the AQI ════════════════
        dbc.Row([dbc.Col(section_title("Rethinking the AQI", align='center'))]),
        dbc.Row([
            dbc.Col(text_card("Why it matters", analysis.PANEL_EXPLORE_EPA),width=4),
            dbc.Col(text_card("Approach", analysis.PANEL_EXPLORE_SUMAQI),width=4),
            dbc.Col(text_card("Example", analysis.PANEL_EXPLORE_SUMAQI_EXAMPLE),width=4),

        ]),
        dbc.Row([
            dbc.Col(epa_report_card(113, "Unhealthy for Sensitive Groups (SG)", analysis.PANEL_EXPLORE_EPA_CARD, "var(--stat-problem-3)"),width=3),
            dbc.Col(graph_card("explore-sum-aqi-graph", explore_sum_aqi, height='360px'), width=9),
        ], align="center"),
        dbc.Row([
            dbc.Col(text_card("Monitor coverage", analysis.PANEL_EXPLORE_PIE), width=4),
            dbc.Col(graph_card("explore-pie-graph", explore_pie, height='360px'), width=8),
        ], align="start"),
        dbc.Row([
            dbc.Col(graph_card("explore-wrong-guide-graph", explore_wrong_guide, height='360px'), width=8),
            dbc.Col(text_card("Reading the examples", analysis.PANEL_EXPLORE_MISCLASS), width=4),
        ], align="start"),
        dbc.Row([
            dbc.Col(text_card("Worst missclassification", analysis.PANEL_WORST_MISSCLASS),width=3),
            dbc.Col(misclass_example_card(misclassification_examples[0]), width=4),
            dbc.Col(misclass_example_card(misclassification_examples[1]), width=5),

        ], className="g-3"),


        # ══ Section 2: Fire Data Cleaning ════════════════
        dbc.Row([dbc.Col(section_title("Fire Data Cleaning", align='center'))]),
        dbc.Row([
            dbc.Col(text_card("Pixel-size filter", analysis.PANEL_EXPLORE_SCANTRACK), width=4),
            dbc.Col(graph_card("explore-scan-track-graph", explore_scan_track, height='420px'), width=8),
        ], align="start"),
        dbc.Row([
            dbc.Col(graph_card("explore-data-entries-graph", explore_data_entries, height='450px'), width=8),
            dbc.Col(text_card("Filtering decisions", analysis.PANEL_EXPLORE_ENTRIES), width=4),
        ], align="start"),
        dbc.Row([
            dbc.Col(text_card("Fire categories", analysis.PANEL_EXPLORE_CATEGORY), width=4),
            dbc.Col(graph_card("explore-category-graph", explore_category, height='500px'), width=8),
        ], align="start"),
    ])

    return behind_data_tab

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
                                        build_intro_tab(),
                                        build_air_quality_tab(),
                                        build_fire_data_tab(),
                                        build_time_serie_event(),
                                        build_behind_data(),
                                        ]),
                                    ],
                                )

    return layout
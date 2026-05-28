from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from dash import Input, Output, callback

from src.display import COLORS_MAP

from data_transforms import *
from figures_aq import make_pollutant_distribution, make_aq_us_plot, compute_max_boxplot
from figures_fire import make_cloropleth_fire_counties, make_bar_fire_event, make_fire_aqi_overlay
from figures_event import make_aq_time_series, make_burning_area_plot, make_overlay_aq_fire


# ============================================================================
#  DASH CALLBACKS
# ============================================================================

def apply_theme(fig, dark_mode):
    fig.update_layout(
        template='plotly_dark' if dark_mode else 'ggplot2',
        legend=dict(
            bgcolor     ='rgba(43,28,26,0.0)'       if dark_mode else 'rgba(255,255,255,0.0)',
            bordercolor ='rgb(91,64,61)'              if dark_mode else 'rgb(227,190,185)',
            font        =dict(color='rgb(220,220,220)' if dark_mode else 'rgb(39,24,22)'),
        ),
    )
    return fig

@callback(Output("page-wrapper", "className"), Input("switch-theme", "value"))
def change_theme(value):
    return "dark" if value else ""

@callback(
    # Tab 1 — AQ Stats
    Output("annual-pollutant-graph",      "figure"),
    Output("pollutant-exceedances-graph",  "figure"),
    Output("pollutant-distribution-graph", "figure"),
    # Tab 2 — Fire Data
    Output("top-counties-graph",          "figure"),
    Output("top-fire-graph",              "figure"),
    Output("overlay-fire-aqi-graph",      "figure"),
    # Tab 4 — Event Dive
    Output("overlay-map-graph",           "figure"),
    Output("ts-site1-graph",              "figure"),
    Output("ts-site2-graph",              "figure"),
    Output("burning-graph",               "figure"),
    Input("switch-theme",                 "value"),
)
def update_figure_theme(dark_mode):
    mapbox_style = 'carto-darkmatter' if dark_mode else 'carto-positron'

    # Tab 1
    fig_pollutant_dist = make_pollutant_distribution(df_aqr_annual)
    fig_us_map         = make_aq_us_plot(df_county_aqr_annual, list_best=['WA', 'ID', 'MS'], list_worst=['CA', 'TX', 'AZ'])
    fig_boxplot        = compute_max_boxplot(df_annual_stats, state_list)
    # Tab 2
    fig_counties       = make_cloropleth_fire_counties(df_fire, ca_geojson)
    fig_top_fires      = make_bar_fire_event(df_biggest_fire)
    fig_fire_aqi       = make_fire_aqi_overlay(df_aq_quantile, df_biggest_fire)
    # Tab 4
    fig_map            = make_overlay_aq_fire(df_day_site_1, df_day_site_2, gdf_fire_day, geojson_fire_dict, mapbox_style=mapbox_style)
    fig_site1          = make_aq_time_series(df_event_site_1, site_1, 'Fresno Area', colors=COLORS_MAP['FRESNO'])
    fig_site2          = make_aq_time_series(df_event_site_2, site_2, 'Sierra National Forest - EAST', colors=COLORS_MAP['SIERRA'])
    fig_burning        = make_burning_area_plot(gdf)

    all_figs = [fig_pollutant_dist, fig_us_map, fig_boxplot,
                fig_counties, fig_top_fires, fig_fire_aqi,
                fig_map, fig_site1, fig_site2, fig_burning]

    for fig in all_figs:
        apply_theme(fig, dark_mode)

    # Map figures: template only (preserve their own legend styles)
    for fig in [fig_us_map, fig_counties, fig_map]:
        fig.update_layout(template='plotly_dark' if dark_mode else 'ggplot2')

    return (fig_pollutant_dist, fig_us_map, fig_boxplot,
            fig_counties, fig_top_fires, fig_fire_aqi,
            fig_map, fig_site1, fig_site2, fig_burning)

from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import json
from dash import Input, Output, callback, Patch, callback_context

from src.display import COLORS_MAP

from data_transforms import *
from figures_aq import make_pollutant_distribution, make_aq_us_plot, compute_max_boxplot
from figures_fire import make_cloropleth_fire_counties, make_bar_fire_event, make_fire_aqi_overlay
from figures_event import (make_aq_time_series, make_burning_area_plot, make_overlay_aq_fire,
                           make_aq_hotspot_trace, make_fire_perimeter_trace)


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
    # Tab 4 — Event Dive (time series + burning area only; map has its own callback)
    Output("ts-site1-graph",              "figure"),
    Output("ts-site2-graph",              "figure"),
    Output("burning-graph",               "figure"),
    Input("switch-theme",                 "value"),
)
def update_figure_theme(dark_mode):
    # Tab 1
    fig_pollutant_dist = make_pollutant_distribution(df_aqr_annual)
    fig_us_map         = make_aq_us_plot(df_county_aqr_annual, list_best=['WA', 'ID', 'MS'], list_worst=['CA', 'TX', 'AZ'])
    fig_boxplot        = compute_max_boxplot(df_annual_stats, state_list)
    # Tab 2
    fig_counties       = make_cloropleth_fire_counties(df_fire, ca_geojson)
    fig_top_fires      = make_bar_fire_event(df_biggest_fire)
    # Tab 4
    fig_site1  = make_aq_time_series(df_event_site_1, site_1, 'Fresno Area', colors=COLORS_MAP['FRESNO'])
    fig_site2  = make_aq_time_series(df_event_site_2, site_2, 'Sierra National Forest - EAST', colors=COLORS_MAP['SIERRA'])
    fig_burning = make_burning_area_plot(gdf)

    all_figs = [fig_pollutant_dist, fig_us_map, fig_boxplot,
                fig_counties, fig_top_fires,
                fig_site1, fig_site2, fig_burning]

    for fig in all_figs:
        apply_theme(fig, dark_mode)

    for fig in [fig_us_map, fig_counties]:
        fig.update_layout(template='plotly_dark' if dark_mode else 'ggplot2')

    return (fig_pollutant_dist, fig_us_map, fig_boxplot,
            fig_counties, fig_top_fires,
            fig_site1, fig_site2, fig_burning)


@callback(
    Output("overlay-map-graph", "figure"),
    Input("date-slider",        "value"),
    Input("switch-theme",       "value"),
)
def update_event_map(slider_idx, dark_mode):
    selected_day = event_dates[slider_idx]
    mapbox_style = 'carto-darkmatter' if dark_mode else 'carto-positron'

    gdf_day      = gdf.loc[gdf['acq_date'] == selected_day]
    geojson_day  = json.loads(gdf_day.to_json())
    df_site1_day = df_event_site_1[df_event_site_1['Date'] == selected_day]
    df_site2_day = df_event_site_2[df_event_site_2['Date'] == selected_day]

    # Slider drag: only patch the three day-specific traces + geojson layer.
    # The two ellipses (traces 0, 1) are static and never change.
    if callback_context.triggered_id == 'date-slider':
        patched = Patch()
        patched['data'][2] = make_aq_hotspot_trace(df_site1_day, 'Fresno',
                                                    show_colorbar=True, show_legend=True)
        patched['data'][3] = make_aq_hotspot_trace(df_site2_day, 'Sierra National Forest (EAST)',
                                                    show_colorbar=False, show_legend=False)
        patched['data'][4] = make_fire_perimeter_trace(gdf_day)
        patched['layout']['mapbox']['layers'] = [dict(
            sourcetype='geojson', source=geojson_day,
            type='fill', color='rgba(255, 100, 0, 0.2)', below='traces',
        )]
        patched['layout']['title']['text'] = f'Fire Perimeter & Air Quality — {selected_day}'
        return patched

    # Theme switch or initial load: full rebuild
    fig = make_overlay_aq_fire(df_site1_day, df_site2_day, gdf_day, geojson_day,
                                selected_day=selected_day, mapbox_style=mapbox_style)
    apply_theme(fig, dark_mode)
    fig.update_layout(template='plotly_dark' if dark_mode else 'ggplot2')
    return fig


@callback(
    Output("overlay-fire-aqi-graph", "figure"),
    Input("pollutant-dropdown",      "value"),
    Input("switch-theme",            "value"),
)
def update_fire_aqi_overlay(pollutant_name, dark_mode):
    col = POLLUTANT_COL_MAP[pollutant_name]
    df_q = compute_aqi_quantiles(col)
    fig = make_fire_aqi_overlay(df_q, df_biggest_fire, pollutant_name=pollutant_name)
    apply_theme(fig, dark_mode)
    return fig

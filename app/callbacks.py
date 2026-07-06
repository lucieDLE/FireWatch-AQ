import path_setup  # noqa: F401

import json
from dash import Input, Output, callback, Patch, callback_context

from src.display import COLORS_MAP

from data_transforms import (
    df_aqi, df_fire, df_aqr_annual, df_county_aqr_annual, df_annual_stats,
    df_biggest_fire, ca_geojson,
    state_list, list_best_codes, list_worst_codes, POLLUTANT_COL_MAP,
    get_event_data, compute_aqi_quantiles, compute_burnt_area_gdf,
)
from figures_aq import make_pollutant_distribution, make_aq_us_plot, compute_max_boxplot
from figures_fire import make_cloropleth_fire_counties, make_bar_fire_event, make_fire_aqi_overlay
from figures_event import (make_aq_time_series, make_burning_area_plot, make_overlay_aq_fire,
                           make_aq_hotspot_trace, make_fire_perimeter_trace)
from figures_explore import (
    make_scan_track_distribution, make_fire_data_entry_analysis, make_fire_category_repartition,
    make_barplot_sum_aqi, make_pollutant_number_pie_chart, make_wrong_guidance_plot,
)
import analysis


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
    # Tab 2 — Fire Data
    Output("top-counties-graph",          "figure"),
    Output("top-fire-graph",              "figure"),
    # Behind the Data — methodology / cleaning figures
    # Output("explore-scan-track-graph",    "figure"),
    # Output("explore-data-entries-graph",  "figure"),
    # Output("explore-category-graph",      "figure"),
    Output("explore-pie-graph",           "figure"),
    Output("explore-wrong-guide-graph",   "figure"),
    Input("switch-theme",                 "value"),
)
def update_figure_theme(dark_mode):
    # Tab 1
    fig_pollutant_dist = make_pollutant_distribution(df_aqr_annual)
    fig_us_map         = make_aq_us_plot(df_county_aqr_annual, list_best=list_best_codes, list_worst=list_worst_codes)
    # Tab 2
    fig_counties       = make_cloropleth_fire_counties(df_fire, ca_geojson)
    fig_top_fires      = make_bar_fire_event(df_biggest_fire)

    all_figs = [fig_pollutant_dist, fig_us_map, fig_counties, fig_top_fires]
    for fig in all_figs:
        apply_theme(fig, dark_mode)
    for fig in [fig_us_map, fig_counties]:
        fig.update_layout(template='plotly_dark' if dark_mode else 'ggplot2')

    # Behind the Data — these handle their own template via dark_mode
    fig_pie          = make_pollutant_number_pie_chart(df_aqi, dark_mode)
    fig_wrong_guide  = make_wrong_guidance_plot(df_aqi, dark_mode)

    return (
        fig_pollutant_dist, fig_us_map, fig_counties, fig_top_fires,
        fig_pie, fig_wrong_guide,
    )


@callback(
    Output("pollutant-distribution-graph", "figure"),
    Output("pollutant-distribution-graph", "style"),
    Output("explore-sum-aqi-graph",        "figure"),
    Output("explore-sum-aqi-graph",        "style"),
    Input("switch-theme",   "value"),
    Input("viewport-width", "data"),
)
def update_responsive_figures(dark_mode, width):
    # Viewport-driven layouts. Bootstrap breakpoints: lg=992, md=768; phone < 768.
    width = width or 1200
    is_phone = width < 768

    # Box-plot facet grid: desktop 3 cols (2 rows), tablet 2 cols (3 rows), phone 1 col (6 rows).
    if width >= 992:
        n_cols = 3
    elif width >= 768:
        n_cols = 2
    else:
        n_cols = 1

    fig_boxplot = compute_max_boxplot(df_annual_stats, state_list, n_cols=n_cols)
    apply_theme(fig_boxplot, dark_mode)
    n_pollutants = df_annual_stats['Parameter Name'].nunique()
    n_rows = -(-n_pollutants // n_cols)  # ceil division
    # taller graph when stacked into more rows so each facet stays readable
    box_height = max(560, 320 * n_rows)

    # Composite AQI: side by side normally, stacked (taller) on phone.
    fig_sum_aqi = make_barplot_sum_aqi(df_aqi, dark_mode, stack=is_phone)
    aqi_height = 650 if is_phone else 450

    return (
        fig_boxplot, {'height': f'{box_height}px'},
        fig_sum_aqi, {'height': f'{aqi_height}px'},
    )


@callback(
    Output("ts-site1-graph",    "figure"),
    Output("ts-site2-graph",    "figure"),
    Output("burning-graph",     "figure"),
    Output("date-slider",       "min"),
    Output("date-slider",       "max"),
    Output("date-slider",       "marks"),
    Output("date-slider",       "value"),
    Output("event-desc-header", "children"),
    Output("event-desc-body",   "children"),
    Output("event-site1-header","children"),
    Output("event-site1-body",  "children"),
    Output("event-site2-header","children"),
    Output("event-site2-body",  "children"),
    Input("fire-dropdown",      "value"),
    Input("switch-theme",       "value"),
)
def update_event_tab(fire_name, dark_mode):
    ev = get_event_data(fire_name)
    dates       = ev['event_dates']
    fig_site1   = make_aq_time_series(ev['df_event_site_1'], ev['site_1'],
                                      site_name=ev['site_name_1'], colors=COLORS_MAP['FRESNO'])
    fig_site2   = make_aq_time_series(ev['df_event_site_2'], ev['site_2'],
                                      site_name=ev['site_name_2'], colors=COLORS_MAP['SIERRA'])
    fig_burning = make_burning_area_plot(ev['gdf'], event_start=ev['EVENT_START'], event_end=ev['EVENT_END'])

    for fig in [fig_site1, fig_site2, fig_burning]:
        apply_theme(fig, dark_mode)

    marks = {i: {'label': dates[i][5:], 'style': {'fontSize': '11px'}}
             for i in range(0, len(dates), 3)}

    panel = analysis.FIRE_EVENT_PANEL_MAP[fire_name]
    desc, site1, site2 = panel

    return (fig_site1, fig_site2, fig_burning,
            0, max(len(dates) - 1, 0), marks, 0,
            desc[0], desc[1], site1[0], site1[1], site2[0], site2[1])


@callback(
    Output("overlay-map-graph", "figure"),
    Input("date-slider",        "value"),
    Input("switch-theme",       "value"),
    Input("fire-dropdown",      "value"),
)
def update_event_map(slider_idx, dark_mode, fire_name):
    ev           = get_event_data(fire_name)
    dates        = ev['event_dates']
    triggered    = callback_context.triggered_id

    # When the fire changes, ignore the stale slider and start from day 0
    if triggered == 'fire-dropdown' or not dates:
        idx = 0
    else:
        idx = min(slider_idx, len(dates) - 1)

    selected_day = dates[idx] if dates else ''
    center_lat   = ev['map_center_lat']
    center_lon   = ev['map_center_lon']

    gdf_day       = ev['gdf'].loc[ev['gdf']['acq_date'] == selected_day]
    gdf_burnt     = compute_burnt_area_gdf(ev['gdf'], selected_day)

    geojson_day   = json.loads(gdf_day.to_json())
    geojson_burnt = json.loads(gdf_burnt.to_json())
    df_site1_day  = ev['df_event_site_1'][ev['df_event_site_1']['Date'] == selected_day]
    df_site2_day  = ev['df_event_site_2'][ev['df_event_site_2']['Date'] == selected_day]

    # Slider drag: patch only the day-specific traces (ellipses 0,1 stay)
    if triggered == 'date-slider':
        patched = Patch()
        patched['data'][2] = make_aq_hotspot_trace(df_site1_day, ev['site_name_1'],
                                                    show_colorbar=True, show_legend=True)
        patched['data'][3] = make_aq_hotspot_trace(df_site2_day, ev['site_name_2'],
                                                    show_colorbar=False, show_legend=False)
        patched['data'][4] = make_fire_perimeter_trace(gdf_burnt, color='amber')
        patched['data'][5] = make_fire_perimeter_trace(gdf_day, color='fire')
        patched['layout']['mapbox']['layers'] = [dict(
            sourcetype='geojson', source=geojson_day,
            type='fill', color='rgba(255, 100, 0, 0.2)', below='traces',
        )]
        patched['layout']['title']['text'] = f'Fire Perimeter & Air Quality <br> {selected_day}'
        return patched

    # Fire change / theme switch / initial load: full rebuild
    fig = make_overlay_aq_fire(df_site1_day, df_site2_day, gdf_day, geojson_day,
                                gdf_burnt, geojson_burnt,
                                selected_day=selected_day,
                                site_name_1=ev['site_name_1'], site_name_2=ev['site_name_2'],
                                center_lat=center_lat, center_lon=center_lon)
    fig.update_layout(
        template='plotly_dark' if dark_mode else 'ggplot2',
        legend=dict(
            bgcolor     ='rgba(255,255,255,1.0)',
            bordercolor ='rgb(91,64,61)'  ,
            font        =dict(color='rgb(39,24,22)'),
        ),
    )
    return fig


@callback(
    Output("overlay-fire-aqi-graph",  "figure"),
    Output("pollutant-card-header",   "children"),
    Output("pollutant-card-body",     "children"),
    Input("pollutant-dropdown",       "value"),
    Input("switch-theme",             "value"),
)
def update_fire_aqi_overlay(pollutant_name, dark_mode):
    col = POLLUTANT_COL_MAP[pollutant_name]
    df_q = compute_aqi_quantiles(col)
    fig = make_fire_aqi_overlay(df_q, df_biggest_fire, pollutant_name=pollutant_name)
    fig = apply_theme(fig, dark_mode)
    panel = analysis.POLLUTANT_PANEL_MAP[pollutant_name]
    return fig, panel[0], panel[1]

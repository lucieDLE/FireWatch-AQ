import plotly.graph_objects as go
from dash import Input, Output, State, callback

import src.config
from figures import *
from data import *

# ============================================================================
#  DASH CALLBACKS
# ============================================================================

def apply_theme(fig, dark_mode):
    """Apply template + legend colors — called after figure is built."""
    fig.update_layout(
        template='plotly_dark' if dark_mode else 'plotly_white',
        legend=dict(
            bgcolor='rgba(30,14,5,0.85)'    if dark_mode else 'rgba(255,255,255,0.85)',
            bordercolor='rgba(100,50,20,0.8)' if dark_mode else 'rgba(180,180,180,0.8)',
            font=dict(color='#ffd6b0' if dark_mode else '#3d0c00'),
        ),
    )
    return fig

@callback(Output("page-wrapper", "className"), Input("switch-theme", "value"))
def change_theme(value):
    return "dark" if value else ""

@callback(
    Output("overlay-map-graph",  "figure"),
    Output("ts-site1-graph",     "figure"),
    Output("ts-site2-graph",     "figure"),
    Output("burning-graph",      "figure"),
    Input("switch-theme",        "value"),
)
def update_figure_theme(dark_mode):
    mapbox_style = 'carto-darkmatter' if dark_mode else 'carto-positron'

    fig_map     = make_overlay_aq_fire(df_day_site_1, df_day_site_2, gdf_fire_day, geojson_fire_dict, mapbox_style=mapbox_style)
    fig_site1   = make_aq_time_series(df_event_site_1, site_1, 'Fresno Area', colors=COLORS_MAP['FRESNO'])
    fig_site2   = make_aq_time_series(df_event_site_2, site_2, 'Sierra National Forest - EAST', colors=COLORS_MAP['SIERRA'])
    fig_burning = make_burning_area_plot(gdf)

    for fig in [fig_map, fig_site1, fig_site2, fig_burning]:
        apply_theme(fig, dark_mode)

    return fig_map, fig_site1, fig_site2, fig_burning

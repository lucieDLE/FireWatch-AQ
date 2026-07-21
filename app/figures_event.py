import path_setup  # noqa: F401

import numpy as np
import plotly.graph_objects as go
import pandas as pd

from src.config import CENTER_LAT, CENTER_LON, FIRE_LAT, FIRE_LON

# Center the map on the fire bounding box
_FIRE_CENTER_LAT = (FIRE_LAT[0] + FIRE_LAT[1]) / 2
_FIRE_CENTER_LON = (FIRE_LON[0] + FIRE_LON[1]) / 2
from src.display import (
    green_colors, red_colors, line_greens, line_reds,
    AQI_CMAP, AQI_BANDS_COLOR, AQI_HOVER_TEMPLATE, AQI_REPORT_COLS,
    FIRE_REPORT_COLS, FIRE_HOVER_TEMPLATE, COLORS_MAP, MARGIN, MARGIN_MAP, TITLE_DICT, LEGEND_BOTTOM
)


def _geoms_to_lines(gdf_wgs84):
    """Extract polygon exterior rings as flat lat/lon lists with None breaks."""
    lats, lons = [], []
    for geom in gdf_wgs84.geometry:
        polys = geom.geoms if geom.geom_type == 'MultiPolygon' else [geom]
        for poly in polys:
            coords = list(poly.exterior.coords)
            lons += [c[0] for c in coords] + [None]
            lats += [c[1] for c in coords] + [None]
    return lats, lons


def make_aq_hotspot_trace(df_day, site_name, show_colorbar=True, show_legend=True):
    df_day = df_day[df_day['max_AQI'] != 'N/A'].copy()
    colorbar = dict(
        title=dict(text='AQI'),
        thickness=14, len=0.5, x=.99, xanchor='right', y=0.5,
        tickvals=[0, 50, 100, 150, 200, 300, 400],
    ) if show_colorbar else {}
    return go.Scattermapbox(
        lat=df_day['Site Latitude'],
        lon=df_day['Site Longitude'],
        mode='markers',
        name='Air Quality Captors',
        marker=dict(
            size=12,
            color=df_day['max_AQI'],
            colorscale=AQI_CMAP,
            cmin=0, cmax=400,
            opacity=0.9,
            colorbar=colorbar,
        ),
        customdata=df_day[AQI_REPORT_COLS],
        hovertemplate=AQI_HOVER_TEMPLATE,
        showlegend=show_legend,
    )


def make_site_ellipse_trace(df_day, color_line, color_fill, name, padding=0.15):
    if df_day.empty:
        return go.Scattermapbox(lat=[], lon=[], mode='lines', name=name,
                                fill='toself', fillcolor=color_fill,
                                line=dict(color=color_line, width=2),
                                hoverinfo='skip', showlegend=True)

    lats = df_day['Site Latitude']
    lons = df_day['Site Longitude']

    center_lat, center_lon = lats.mean(), lons.mean()
    r_lat = (lats.max() - lats.min()) / 2 + padding
    r_lon = (lons.max() - lons.min()) / 2 + padding

    theta = np.linspace(0, 2 * np.pi, 120)
    ell_lats = (center_lat + r_lat * np.sin(theta)).tolist()
    ell_lons = (center_lon + r_lon * np.cos(theta)).tolist()

    return go.Scattermapbox(
        lat=ell_lats, lon=ell_lons,
        mode='lines',
        fill='toself',
        fillcolor=color_fill,
        line=dict(color=color_line, width=2),
        name=name,
        hoverinfo='skip',
        showlegend=True,
    )


def make_fire_perimeter_trace(gdf, color='fire'):
    if gdf.empty:
        return go.Scattermapbox(lat=[], lon=[], mode='lines', name='Fire perimeter', showlegend=True)

    perim_lats, perim_lons = _geoms_to_lines(gdf)
    n_pts = len(perim_lats)
    cd_vals = np.tile(gdf[FIRE_REPORT_COLS].round(1).values[0], (n_pts, 1))

    if color=='amber':
        line_color =  'rgba(50,50,50,1.0)'
        fill_color = 'rgba(50,50,50,0.7)'
        name = 'Inactive Fire (Burnt area)'
    else:
        line_color = COLORS_MAP['FIRE'][1]
        fill_color = 'rgba(253,141,60,0.7)'
        name = 'Active Fire (Burning area)'

    return go.Scattermapbox(
        lat=perim_lats, lon=perim_lons,
        mode='lines',
        fill='toself',
        fillcolor=fill_color,
        line=dict(width=1.5, color=line_color),
        name=name,
        customdata=cd_vals,
        hovertemplate=FIRE_HOVER_TEMPLATE,
    )


def make_aq_time_series(df, sites, site_name, colors, legend_entrywidth=0.33):
    fig = go.Figure()
    for idx, site_id in enumerate(sites):
        df_site = df.loc[df['Site ID'] == site_id]
        if df_site.empty:
            continue
        fig.add_trace(go.Scatter(
            x=df_site['Date'],
            y=df_site['max_AQI'],
            name=df_site.iloc[0]['Local Site Name'],
            line_color=colors[idx] if idx < len(colors) else None,
        ))

    for y0, y1, color in AQI_BANDS_COLOR:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=color, line_width=0, layer='below')

    fig.update_layout(
        title=dict(text=f'AQI at selected sites near: <br> {site_name}',**TITLE_DICT),
        xaxis=dict(title_text='Date'),
        yaxis=dict(title_text='Air Quality Index (AQI)'),
        hovermode='x unified',
        legend={**LEGEND_BOTTOM, 'maxheight': 0.12,
                'entrywidthmode': 'fraction', 'entrywidth': legend_entrywidth},
        margin=MARGIN,
    )
    return fig


def make_burning_area_plot(gdf, event_start=None, event_end=None):
    plot_df = gdf[['acq_date', 'area_km2', 'perimeter_km']].copy()

    if event_end:
        last_date = pd.to_datetime(plot_df['acq_date'].max())
        day_after = (last_date + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        zeros = pd.DataFrame({'acq_date': [day_after, event_end], 'area_km2': [0, 0], 'perimeter_km': [0, 0]})
        plot_df = pd.concat([plot_df, zeros], ignore_index=True)

    fig = go.Figure([
        go.Scatter(x=plot_df['acq_date'], y=plot_df['area_km2'],
                   name='Burning Area (km²)', line_color=COLORS_MAP['FIRE'][0]),
        go.Scatter(x=plot_df['acq_date'], y=plot_df['perimeter_km'],
                   name='Fire Perimeter (km)', line_color=COLORS_MAP['FIRE'][1]),
    ])
    fig.update_layout(
        title=dict(text='Estimated Burning Area <br> and Fire Perimeter', **TITLE_DICT),
        hovermode='x unified',
        xaxis=dict(title_text='Date', range=[event_start, event_end] if event_start else None),
        legend=LEGEND_BOTTOM,
        margin=MARGIN,
    )
    return fig


def make_overlay_aq_fire(df_day_site_1, df_day_site_2, gdf_fire_day, geojson_fire_dict,gdf_burnt_area, geojson_burnt_dict,
                         selected_day='', site_name_1='Site 1', site_name_2='Site 2', center_lat=None, center_lon=None):
    map_center_lat = center_lat if center_lat is not None else _FIRE_CENTER_LAT
    map_center_lon = center_lon if center_lon is not None else _FIRE_CENTER_LON

    fig = go.Figure(data=[
        make_site_ellipse_trace(df_day_site_1, 'rgba(34,120,50,0.9)', 'rgba(34,120,50,0.10)',
                                f'Monitoring Site 1: {site_name_1}', padding=0.2),
        make_site_ellipse_trace(df_day_site_2, 'rgba(72,105,140,0.9)', 'rgba(72,105,140,0.08)',
                                f'Monitoring Site 2: {site_name_2}', padding=0.3),
        make_aq_hotspot_trace(df_day_site_1, site_name_1, show_colorbar=True, show_legend=True),
        make_aq_hotspot_trace(df_day_site_2, site_name_2, show_colorbar=False, show_legend=False),
        make_fire_perimeter_trace(gdf_burnt_area, color='amber'),
        make_fire_perimeter_trace(gdf_fire_day, color='fire'),

    ])

    fig.update_layout(
        title=dict(
            text=f'Fire Perimeter & Air Quality — {selected_day}',
            **TITLE_DICT,
        ),
        mapbox=dict(
            style='open-street-map',
            layers=[dict(
                sourcetype='geojson',
                source=geojson_fire_dict,
                type='fill',
                color='rgba(255, 100, 0, 0.2)',
                below='traces',
            )],
            center=dict(lat=map_center_lat, lon=map_center_lon),
            zoom=7,
        ),
        margin=MARGIN_MAP,
        legend=dict(
            bgcolor='rgba(255, 255, 255, 0.85)',
            bordercolor='rgba(180, 180, 180, 0.8)',
            borderwidth=1,
            x=0.01, y=0.99,
            xanchor='left', yanchor='top',
            font=dict(size=12),
            itemsizing='constant',
        ),
    )
    return fig

def make_satellite_map(gdf_ca_cities, dict_satellite,
                        center_lat=None, center_lon=None, selected_day=''):
    map_center_lat = center_lat if center_lat is not None else _FIRE_CENTER_LAT
    map_center_lon = center_lon if center_lon is not None else _FIRE_CENTER_LON

    if dict_satellite is None:
        return go.Figure()

    fig = go.Figure(
        go.Scattermapbox(
            lat=gdf_ca_cities['lat'],
            lon=gdf_ca_cities['lon'],
            mode='markers+text',
            text=gdf_ca_cities['City'],
            textposition='top center',
            marker=dict(size=6, color='fuchsia'),
            name='Cities',
        )
    )

    coords = dict_satellite['coordinates']

    lon_min, lon_max = coords[0][0], coords[1][0]
    lat_min, lat_max = coords[2][1], coords[1][1]

    lon_span = abs(lon_max - lon_min)
    lat_span = abs(lat_max - lat_min)
    mid_lat = (lat_min + lat_max) / 2
    mid_lon = (lon_min + lon_max) / 2

    # 1 deg lon is narrower than 1 deg lat by cos(lat), so scale width to match
    aspect = (lon_span * np.cos(np.radians(mid_lat))) / lat_span

    base_height = 600
    fig_width = base_height * aspect

    # Web-Mercator: the world is 512 px wide at zoom 0 and doubles each level.
    # Pick the zoom where lon_span exactly fills the figure width.
    zoom = np.log2(fig_width * 360.0 / (512.0 * lon_span))

    fig.update_layout(
        title=dict(text=f'Satellite Imagery — {selected_day}', **TITLE_DICT),
        mapbox=dict(
            style='white-bg',
            center=dict(lat=mid_lat, lon=mid_lon),
            zoom=zoom,
            layers=[dict(
                sourcetype='image',
                source=dict_satellite['source'],
                coordinates=dict_satellite['coordinates'],
                below='traces',
            )],
        ),
        height=base_height,
        width=fig_width,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig
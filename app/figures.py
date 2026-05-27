from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.config import *
from src.display import *
import pandas as pd 
import plotly.graph_objects  as go
from plotly.subplots import make_subplots
import plotly.express as px
import urllib.request

import numpy as np
import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import Point
from shapely.ops import unary_union
import plotly.graph_objects as go
import plotly.express as px

# made from :
# from https://colorbrewer2.org/


def geoms_to_lines(gdf_wgs84):
    """Extract polygon exterior rings as flat lat/lon lists with None breaks."""
    lats, lons = [], []
    for geom in gdf_wgs84.geometry:
        polys = geom.geoms if geom.geom_type == 'MultiPolygon' else [geom]
        for poly in polys:
            coords = list(poly.exterior.coords)
            lons += [c[0] for c in coords] + [None]
            lats += [c[1] for c in coords] + [None]
    return lats, lons


def make_fire_category_repartition(df, df_cleaned):

    fig = make_subplots(
        rows=1, cols=5,
        column_widths=[0.2, 0.2, 0.2, 0.2, 0.2],
        subplot_titles=FIRE_CAT_NAMES,
        shared_yaxes=False,
    )

    for idx in range(len(FIRE_CAT_NAMES)):
        df_cat = df.loc[df.fire_cat == idx]

        fig.add_trace(go.Box(
            y=df_cat['frp'],
            name='Raw',
            legendgroup='Raw',
            showlegend=(idx == 0),
            fillcolor=green_colors[idx+1],
            line=dict(color=line_greens[idx+1]),
            marker_size=3, line_width=1,
            jitter=1.0, whiskerwidth=0.2,
        ), row=1, col=idx + 1)

        if idx != 0:
            df_cleaned_cat = df_cleaned.loc[df_cleaned.fire_cat == idx]
            fig.add_trace(go.Box(
                y=df_cleaned_cat['frp'],
                name='Cleaned',
                legendgroup='Cleaned',
                showlegend=(idx == 1),
                fillcolor=red_colors[idx+1],
                line=dict(color=line_reds[idx+1]),
                marker_size=3, line_width=1,
                jitter=1.0, whiskerwidth=0.2,
            ), row=1, col=idx + 1,)
        

    fig.update_traces(showlegend=False) # remove the clean and raw


    # add custom legend
    for idx, legend_category in enumerate(legend):
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=12, color=green_colors[idx+1], symbol='square', line_width=1, line_color=line_greens[idx+1]),
            name=legend_category,
    ))
    fig.update_layout(
        template='plotly_dark',
        title_text='Fire Repartition by Category and FRP',
        height=500,
    )
    fig.update_yaxes(title_text='FRP (MW)', col=1)

    return fig

def make_fire_data_entry_analysis(df):
    fig = make_subplots(
        rows=1, cols=3,
        column_widths=[0.33, 0.33, 0.33],
        subplot_titles=['Fire pixels by Day/Night', 'Fires Types', 'Confidence Levels'],
        shared_yaxes=False,
    )

    # Panel 1 — Day/Night
    for label, mask, color in [
        ('True Fire (isFire=1)',      df['isFire'] == 1, red_colors[-1]),
        ('Misclassified (isFire=0)',  df['isFire'] == 0, red_colors[2]),
    ]:
        fig.add_trace(go.Histogram(
            x=df.loc[mask, 'daynight'], name=label,
            marker_color=color, opacity=0.85,
            legend='legend2',
        ), row=1, col=1)

    # Panel 2 — Types (numeric x so bars land at 0/1/2/3)
    for type_val, label, color in [
        (0, '0: Vegetation Fire', red_colors[-1]),
        (1, '1: Volcano',         red_colors[2]),
        (2, '2: Static',          red_colors[2]),
        (3, '3: Offshore',        red_colors[2]),
    ]:
        subset = df.loc[df['type'] == type_val, 'type']
        if len(subset) > 0:
            fig.add_trace(go.Histogram(
                x=subset, name=label,
                marker_color=color, opacity=0.85,
                legend='legend3',
            ), row=1, col=2)

    # Panel 3 — Confidence
    for conf_val, label, color in [
        ('l', 'l: low confidence',     red_colors[2]),
        ('n', 'n: nominal confidence', red_colors[-1]),
        ('h', 'h: high confidence',    red_colors[-1]),
    ]:
        fig.add_trace(go.Histogram(
            x=df.loc[df['confidence'] == conf_val, 'confidence'], name=label,
            marker_color=color, opacity=0.85,
            legend='legend4',
        ), row=1, col=3)

    # Global top legend — Kept vs Removed
    for label, color in [('Kept in dataset', red_colors[-1]), ('Removed from dataset', red_colors[2])]:
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode='markers',
            marker=dict(symbol='square', size=10, color=color),
            name=label, legend='legend',
        ))

    fig.update_layout(
        template='plotly_dark',
        title_text='Data Entries and filtering decisions',
        barmode='overlay',
        height=450,
        bargap=0.2,
        yaxis_title='Number of pixels',
        legend =dict(orientation='h', x=0.90, y=1.30, xanchor='left', bgcolor='rgba(0,0,0,0)'),
        legend2=dict(
            orientation="h",
            yanchor='bottom',
            xanchor='left',   
            y=-0.25,
            x=0, 
            bgcolor='rgba(0,0,0,0.3)', 
            borderwidth=0),

        legend3=dict(
            orientation="h",
            yanchor='bottom',
            xanchor='center',   
            y=-0.25,
            x=0.5, 
            bgcolor='rgba(0,0,0,0.3)', 
            borderwidth=0),

        legend4=dict(
                orientation="h",
                yanchor='bottom',
                xanchor='left',   
                y=-0.25,
                x=0.7, 
                bgcolor='rgba(0,0,0,0.3)', 
                borderwidth=0),
    )

    return fig

def make_scan_track_distribution(df):
    fig = go.Figure([
        go.Histogram(x=df["scan"], name='scan', marker_color=red_colors[2], opacity=.8),
        go.Histogram(x=df["track"], name='track', marker_color=red_colors[-1], opacity=.8),
        ],)

    fig.add_vline(x=0.6, line_width=3, line_dash="dash", line_color=line_reds[-1], annotation_text='threshold')
    fig.update_layout(
        template='plotly_dark',
        title_text='Scan and Track distribution',
        bargap=0.3, # gap between bars of adjacent location coordinates
        bargroupgap=0, # gap between bars of the same location coordinates
    )
    fig.update_yaxes(title_text='Number of pixels')
    fig.update_xaxes(title_text='pixel size')

    return fig


def make_pollutant_distribution(df):

    fig = go.Figure()
    fig = px.histogram(df, x="State Name",color='Parameter Name',color_discrete_sequence=red_colors[::-1],height=400)

    fig.update_layout(
        template='plotly_dark',
        barmode='stack', 
        xaxis={'categoryorder':'total descending'},
        title_text='Pollutant Distribution across states ',
        legend=dict(yanchor='top', xanchor='right', title_text=''),
    )
    fig.update_xaxes(tickangle=45)
    return fig


def make_aq_us_plot(df_county, list_best = ['WA', 'ID', 'MS'], list_worst=['CA', 'TX', 'AZ']):

    df_no_exceed = df_county.loc[df_county['primary_exceedance'] == 0]
    df_exceed = df_county.loc[df_county['primary_exceedance'] >0]

    df_no_exceed = df_no_exceed.loc[df_no_exceed['observation'] > 1000]
    df_exceed = df_exceed.loc[df_exceed['primary_exceedance'] > 5]

    sizeref = 2. * df_county['primary_exceedance'].max() / (22 ** 2)
    sizeref_2 = 2. * df_no_exceed['observation'].max() / (22 ** 2)

    fig = go.Figure()
    # --- State fills (drawn first so scatter points appear on top) ---
    fig.add_trace(go.Choropleth(
        name='Worst states',
        locationmode='USA-states',
        locations=list_worst,
        z=[1, 1, 1],
        colorscale=[[0, 'rgba(120,70,150,0.)'], [1, 'rgba(120,70,150,0.)']],
        showlegend=False,
        showscale=False,
        marker_line_color=red_colors[-2],
        marker_line_width=1.5,
    ))

    fig.add_trace(go.Choropleth(
        name='Cleanest states',
        locationmode='USA-states',
        locations=list_best,
        z=[1, 1, 1],
        colorscale=[[0, 'rgba(44,162,95,0.)'], [1, 'rgba(44,162,95,0.)']],
        showscale=False,
        showlegend=False,
        marker_line_color=green_colors[-2],
        marker_line_width=1.5,
    ))


    # --- County-level scatter points ---
    fig.add_trace(go.Scattergeo(
        name='Exceedance recorded',
        locationmode='USA-states',
        lon=df_exceed['longitude'],
        lat=df_exceed['latitude'],
        customdata=df_exceed[['County Name', 'State Name', 'primary_exceedance', 'observation']].values,
        hovertemplate=(
            '<b>%{customdata[0]}</b>, %{customdata[1]}<br>'
            'Exceedances recorded: %{customdata[2]:.0f}<br>'
            'Total observations: %{customdata[3]:,.0f}'
            '<extra></extra>'
        ),
        marker=dict(
            size=df_exceed['primary_exceedance'] / sizeref,
            line_color=line_reds[-3],
            line_width=.8,
            sizemode='area',
            color=red_colors[-3],
            opacity=1.0,
        ),
    ))

    fig.add_trace(go.Scattergeo(
        name='No exceedance',
        locationmode='USA-states',
        lon=df_no_exceed['longitude'],
        lat=df_no_exceed['latitude'],
        customdata=df_no_exceed[['County Name', 'State Name', 'primary_exceedance', 'observation']].values,
        hovertemplate=(
            '<b>%{customdata[0]}</b>, %{customdata[1]}<br>'
            'Exceedances recorded: 0<br>'
            'Total observations: %{customdata[3]:,.0f}'
            '<extra></extra>'
        ),
        marker=dict(
            size=df_no_exceed['observation'] / sizeref_2,
            line_color=line_greens[-2],
            line_width=.5,
            sizemode='area',
            color=green_colors[2],
            opacity=.8,
        ),
    ))

    # # --- Custom square legend entries for state fills ---
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        name='Worst states (CA, TX, AZ)',
        marker=dict(symbol='square', size=12, color="rgba(120,70,150,0.)", line=dict(color=line_reds[-2], width=1.5)),
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        name='Best states (WA, ID, MS)',
        marker=dict(symbol='square', size=12, color="rgba(120,70,150,0.)", line=dict(color=line_greens[-2], width=1.5)),
    ))


    fig.update_layout(
        template = 'plotly_dark',
        # template = 'ggplot2',

        title=dict(
            text='County-level Pollutant Exceedances<br>(Click legend to toggle traces)',
            x=0.5,
            xanchor='center',
        ),
        showlegend=True,
        legend=dict(
            borderwidth=0,
            x=1,
            y=0.5,
            xanchor='right',
            yanchor='middle',
        ),
        geo=dict(
            scope='usa',
            subunitcolor='rgb(100,100,100)',
            domain=dict(x=[0, 0.78], y=[0, 1]),
        ),
        margin=dict(l=0, r=80, t=40, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_xaxes()
    return fig


def compute_max_boxplot(df_stats, states_list):

    custom_colors = green_colors[0:3] + red_colors[0:3]
    custom_lines  = line_greens[0:3] + line_reds[0:3]

    pollutants_list = df_stats['Parameter Name'].unique()

    fig = make_subplots(
        rows=1, cols=len(pollutants_list),
        column_widths=[0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
        subplot_titles=pollutants_list,)

    for col_idx, pollutant in enumerate(pollutants_list):
        for idx, state_name in enumerate(states_list):
            df_ca_pm = df_stats.loc[(df_stats['State Name'] == state_name) & (df_stats['Parameter Name'] == pollutant)]
            
            df_maxes = df_ca_pm[['1st Max Value', '2nd Max Value', '3rd Max Value', '4th Max Value']]
            np_maxes = df_maxes.to_numpy().reshape(-1)
            if len(np_maxes) > 5:

                fig.add_trace(go.Box(y=np_maxes,
                    name=state_name,
                    showlegend=(col_idx == 0),
                    fillcolor=custom_colors[idx],
                    line=dict(color=custom_lines[idx]),
                    marker_size=3, line_width=1,
                    whiskerwidth=0.5,
                ), row=1, col=col_idx + 1)
            else:

                fig.add_trace(go.Box(y=np_maxes,
                    name=state_name,
                    boxpoints='all',
                    showlegend=(col_idx == 0),
                    fillcolor='rgba(255,255,255,0)', ## force opacity to 0 to remove the box
                    line=dict(color='rgba(255,255,255,0)'),
                    marker_size=3, line_width=1,
                    marker=dict(color=custom_lines[idx]),

                ), row=1, col=col_idx + 1)

        fig.add_hline(y=POLLUTANT_THRESHOLDS[pollutant][0],
            line_width=2, line_dash="dash", 
            line_color=red_colors[-1],
            showlegend=(col_idx == 0), 
            opacity=0.8,
            name='guideline threshold',
            annotation_text=f'{POLLUTANT_THRESHOLDS[pollutant][0]} {POLLUTANT_THRESHOLDS[pollutant][1]}',  
            annotation_position="top left",
            row=1, col=col_idx + 1)


    fig.update_layout(
        template='plotly_dark',
        # template='ggplot2',
        title_text='Pollutant distribution by state',
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.12,
            xanchor='center',
            x=0.5,
        ),
    )
    fig.update_xaxes(showticklabels=False)
    return fig

def make_aqi_timeserie(df_q, df_biggest_fire):

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_q['Date'], y=df_q['Q1_smooth'],
        mode='lines', name='10th pct',
        line=dict(color=green_colors[2], width=0),  # invisible border
        showlegend=False,
    ))

    fig.add_trace(go.Scatter(
        x=df_q['Date'], y=df_q['Q3_smooth'],
        mode='lines', name='10th-90th range',
        fill='tonexty',
        fillcolor=green_colors[2].replace('0.8', '0.4'),
        opacity=0.2,
        line=dict(color=green_colors[0], width=0),  # invisible border
    ))

    fig.add_trace(go.Scatter(
            x=df_q['Date'], 
            y=df_q['Q2_smooth'],
            mode='lines',
            name='50th percentile',
            line_color=line_greens[2],
            ))

    fig.add_trace(go.Scatter(
            x=df_q['Date'], 
            y=df_q['Q99_smooth'],
            mode='lines',
            name='99th percentile',
            line_color=line_reds[2],
            ))

    fig.add_trace(go.Scatter(
        x=df_biggest_fire['date'],
        y=df_biggest_fire['acres'],
        mode='markers+text',
        name='Major fires',
        marker=dict(
            symbol='star',
            size=16,
            color=red_colors[2],
            line=dict(color=line_reds[2], width=1),
        ),
        textposition='top center',
        textfont=dict(size=10, color='white'),
        customdata=df_biggest_fire[['poly_IncidentName', 'acres']],
        hovertemplate='<b>%{customdata[0]}</b><br>Date: %{x|%Y-%m-%d}<br>Acres: %{customdata[1]:,.0f}<extra></extra>',
    ), secondary_y=True)

    # ── Health threshold lines ────────────────────────────────────────────────
    for y, label in [(101, 'Unhealthy for sensitive groups'), (151, 'Unhealthy for all')]:
        fig.add_hline(
            y=y, secondary_y=False,
            line=dict(dash='dash', color=line_reds[-2], width=1.5),
            opacity=0.7,
            annotation_text=label,
            annotation_position='top right',
        )

    # ── Layout ────────────────────────────────────────────────────────────────
    fig.update_layout(
        # template='ggplot2',
        template='plotly_dark',
        title_text='PM2.5 AQI vs Fire Activity — California 2025',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
        barmode='overlay',
        margin=dict(t=100),
    )
    fig.update_yaxes(title_text='PM2.5 AQI', secondary_y=False)
    fig.update_yaxes(title_text='Acres Burnt', secondary_y=True, showgrid=False)
    fig.update_xaxes(title_text='Date')

    return fig


def make_aq_hotspot_fig(df_day, site_name, show_colorbar=True, show_legend=True):
    df_day = df_day[df_day['max_AQI'] != 'N/A'].copy()
    colorbar = dict(
        title=dict(text='AQI', font=dict(size=11)),
        thickness=14,
        len=0.5,
        x=.99,
        xanchor='right',
        y=0.5,
        tickvals=[0, 50, 100, 150, 200, 300, 400],
    ) if show_colorbar else {}
    return go.Scattermapbox(
        lat=df_day['Site Latitude'],
        lon=df_day['Site Longitude'],
        mode='markers',
        name=f'Air Quality Captors',
        marker=dict(
            size=12,
            color=df_day['max_AQI'],
            colorscale=AQI_CMAP,
            cmin=0,
            cmax=400,
            opacity=0.9,
            colorbar=colorbar,
        ),
        customdata=df_day[AQI_REPORT_COLS],
        hovertemplate=AQI_HOVER_TEMPLATE,
        showlegend=show_legend,  # add legend only one time
    )

def make_site_ellipse(df_day, color_line, color_fill, name, padding=0.15):
    lats = df_day['Site Latitude']
    lons = df_day['Site Longitude']

    center_lat, center_lon = lats.mean(), lons.mean()
    r_lat = (lats.max() - lats.min()) / 2 + padding
    r_lon = (lons.max() - lons.min()) / 2 + padding

    theta = np.linspace(0, 2 * np.pi, 120)
    ell_lats = (center_lat + r_lat * np.sin(theta)).tolist()
    ell_lons = (center_lon + r_lon * np.cos(theta)).tolist()

    return go.Scattermapbox(
        lat=ell_lats,
        lon=ell_lons,
        mode='lines',
        fill='toself',
        fillcolor=color_fill,
        line=dict(color=color_line, width=2),
        name=name,
        hoverinfo='skip',
        showlegend=True,
    )

def make_aq_time_series(df, sites, site_name, colors, legend_entrywidth=0.33):
    fig = go.Figure()
    for idx, site_id in enumerate(sites):
        df_site = df.loc[df['Site ID'] == site_id] # Long Beach
        fig.add_trace(go.Scatter(x=df_site['Date'], 
                                y=df_site['max_AQI'], 
                                name=df_site.iloc[0]['Local Site Name'], 
                                line_color = colors[idx], 
                                ))

    for y0, y1, color in AQI_BANDS_COLOR:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=color, line_width=0, layer='below')


    fig.update_layout(
        title=dict(
            text=f'AQI at selected sites near: {site_name}',
            yanchor='top', 
            y=0.95,
        ),
        xaxis=dict(title_text="Date"),
        yaxis=dict(title_text="Air Quality Index (AQI)"),
        legend=dict(
            orientation="h",
            yanchor='bottom',
            xanchor='left',   
            y=1.02,
            x=0,
            maxheight=0.12,
            entrywidthmode='fraction',
            entrywidth=legend_entrywidth,
        ),
        margin=dict(l=10, r=10, t=100, b=10),
    )
    return fig

def make_fire_perimeter_plot(gdf):
    # if there is no fire
    if gdf.empty:
        return go.Scattermapbox(lat=[], lon=[], mode='lines', name='Fire perimeter', showlegend=True)

    perim_lats, perim_lons = geoms_to_lines(gdf)
    n_pts = len(perim_lats)
    cd_vals = np.tile(gdf[FIRE_REPORT_COLS].round(1).values[0], (n_pts, 1))

    return go.Scattermapbox(
        lat=perim_lats,
        lon=perim_lons,
        mode='lines',
        fill='toself',
        fillcolor="rgba(253,141,60,0.2)",
        line=dict(width=1.5, color=COLORS_MAP['FIRE'][1]),
        name='Fire perimeter',
        customdata=cd_vals,
        hovertemplate=FIRE_HOVER_TEMPLATE,
    )

def make_burning_area_plot(gdf):

    fig =  go.Figure([
                        go.Scatter( x=gdf['acq_date'], 
                                    y=gdf['area_km2'], 
                                    name = 'Burning Area (km2)',
                                    line_color = COLORS_MAP['FIRE'][0], 
                                    ),
                        go.Scatter( x=gdf['acq_date'], 
                                    y=gdf['perimeter_km'], 
                                    name= 'Fire Perimeter (km)',
                                    line_color = COLORS_MAP['FIRE'][1],
                                    ),
                    ])

    fig.update_layout(
        title=dict(text=f'Estimated Burning Area and Fire Perimeter', yanchor='top', y=0.95,),
        xaxis=dict(title_text="Date"),
        legend=dict(orientation="h",
                    yanchor="top",
                    y=1.2,
                    xanchor="left",
                    maxheight=0.1,
                    ),
        margin=dict(l=10, r=10, t=75, b=10),
    )
    return fig

def make_overlay_aq_fire(df_day_site_1, df_day_site_2, gdf_fire_day, geojson_fire_dict, mapbox_style='carto-positron'):
    fig = go.Figure(data=[
            make_site_ellipse(df_day_site_1, 'rgba(34,120,50,0.9)', 'rgba(34,120,50,0.10)',
                            'Monitoring Site 1: Fresno', padding=0.2),
            make_site_ellipse(df_day_site_2, 'rgba(72,105,140,0.9)', 'rgba(72,105,140,0.08)',
                            'Monitoring Site 2: Sierra National Forest (EAST)', padding=0.3),
            make_aq_hotspot_fig(df_day_site_1, 'Fresno', show_colorbar=True, show_legend=True),
            make_aq_hotspot_fig(df_day_site_2, 'Sierra National Forest (EAST)', show_colorbar=False, show_legend=False),
            make_fire_perimeter_plot(gdf_fire_day),
            ],)


    fig.update_layout(
            title=dict(
                text=f'Fire Perimeter & Air Quality — {SELECTED_DAY}',
                font=dict(size=15), x=0.5, xanchor='center',
            ),
            mapbox=dict(
                style=mapbox_style,
                layers=[dict(
                    sourcetype='geojson',
                    source=geojson_fire_dict,
                    type='fill',
                    color='rgba(255, 100, 0, 0.2)',
                    below='traces',
                )],
                center=dict(lat=CENTER_LAT, lon=CENTER_LON),
                zoom=7,
            ),
            margin=dict(l=10, r=10, t=50, b=10),
            legend=dict(
                bgcolor='rgba(255, 255, 255, 0.85)',
                bordercolor='rgba(180, 180, 180, 0.8)',
                borderwidth=1,
                x=0.01,
                y=0.99,
                xanchor='left',
                yanchor='top',
                font=dict(size=12),
                itemsizing='constant',
            ),
        )
    return fig


def make_cloropleth_fire_counties(df):
    with urllib.request.urlopen(
        "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/california-counties.geojson"
    ) as f:
        ca_geojson = json.load(f)

    ca_counties = gpd.GeoDataFrame.from_features(ca_geojson["features"], crs="EPSG:4326")[
        ["name", "geometry"]
    ]

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs="EPSG:4326",
    )
    gdf = gdf[['latitude', 'longitude','acq_date', 'acq_time', 'frp','isFire', 'fire_cat', 'geometry',
       'poly_IncidentName', 'poly_GISAcres', 'attr_FireCause', 'attr_POOState',
       'attr_POOCounty', 'attr_FireDiscoveryDateTime', 'attr_FireOutDateTime',
       'in_named_fire']]
    joined = gpd.sjoin(gdf, ca_counties, how="left", predicate="within")
    county_counts = (
        joined.groupby("name", dropna=True)["fire_cat"]
        .sum()
        .reset_index(name="fire_score")
        .sort_values("fire_score", ascending=False)
    )

    fig = px.choropleth_map(
        county_counts,
        geojson=ca_geojson,
        locations="name",
        featureidkey="properties.name",
        color="fire_score",
        color_continuous_scale="YlOrRd",
        map_style="dark",
        zoom=4.5,
        center={"lat": CENTER_LAT, "lon": CENTER_LON},
        opacity=0.7,
        labels={"fire_score": "Fire activity score"},
        title="Fire activity score by county (weighted by fire category)",
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    return fig


def make_bar_fire_event(df_biggest_fire):


    fig = px.bar(
        df_biggest_fire,
        x="label", y="acres",
        color="acres", color_continuous_scale=red_colors,
        labels={"label": "Fire Event", "acres": "Estimated burnt acres"},
        title="Top 10 California Fires in 2025",
    )
    fig.update_layout(
        template='plotly_dark',
        coloraxis_showscale=False,
        xaxis_tickangle=-30,
        margin=dict(l=10, r=10, t=50, b=10),
    )

    return fig


def make_fire_aqi_overlay(df_aq_quantile, df_biggest_fire):
    fig = make_subplots(specs=[[{'secondary_y': True}]])

    # ── AQI band (left y-axis) ────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=df_aq_quantile['Date'], y=df_aq_quantile['Q1_smooth'],
        mode='lines', name='Q1 (25th pct)',
        line=dict(color=green_colors[2], width=0),
        showlegend=False,
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df_aq_quantile['Date'], y=df_aq_quantile['Q3_smooth'],
        mode='lines', name='Q1–Q3 band',
        fill='tonexty',
        fillcolor=green_colors[2].replace('0.8', '0.25'),
        line=dict(color=green_colors[0], width=0),
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df_aq_quantile['Date'], y=df_aq_quantile['Q2_smooth'],
        mode='lines', name='AQI median (50th pct)',
        line=dict(color=line_greens[2], width=1.5),
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df_aq_quantile['Date'], y=df_aq_quantile['Q99_smooth'],
        mode='lines', name='AQI 99th pct',
        line=dict(color=line_reds[2], width=1.5),
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=df_biggest_fire['date'],
        y=df_biggest_fire['acres'],
        mode='markers+text',
        name='Major fires',
        marker=dict(
            symbol='star',
            size=16,
            color=red_colors[2],
            line=dict(color=line_reds[2], width=1),
        ),
        # text=df_biggest_fire['poly_IncidentName'],
        textposition='top center',
        textfont=dict(size=10, color='white'),
        customdata=df_biggest_fire[['poly_IncidentName', 'acres']],
        hovertemplate='<b>%{customdata[0]}</b><br>Date: %{x|%Y-%m-%d}<br>Acres: %{customdata[1]:,.0f}<extra></extra>',
    ), secondary_y=True)

    # ── Health threshold lines ────────────────────────────────────────────────
    for y, label in [(101, 'Unhealthy for sensitive groups'), (151, 'Unhealthy for all')]:
        fig.add_hline(
            y=y, secondary_y=False,
            line=dict(dash='dash', color=line_reds[-2], width=1.5),
            opacity=0.7,
            annotation_text=label,
            annotation_position='top right',
        )

    # ── Layout ────────────────────────────────────────────────────────────────
    fig.update_layout(
        template='plotly_dark',
        title_text='PM2.5 AQI vs Fire Activity — California 2025',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
        barmode='overlay',
        margin=dict(t=100),
    )
    fig.update_yaxes(title_text='PM2.5 AQI', secondary_y=False)
    fig.update_yaxes(title_text='Acres Burnt', secondary_y=True, showgrid=False)
    fig.update_xaxes(title_text='Date')
    
    return fig
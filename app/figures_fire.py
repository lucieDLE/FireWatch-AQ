from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from src.config import CENTER_LAT, CENTER_LON
from src.display import green_colors, red_colors, line_greens, line_reds


def make_cloropleth_fire_counties(df, ca_geojson):
    ca_counties = gpd.GeoDataFrame.from_features(ca_geojson['features'], crs='EPSG:4326')[
        ['name', 'geometry']
    ]

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs='EPSG:4326',
    )
    gdf = gdf[[
        'latitude', 'longitude', 'acq_date', 'acq_time', 'frp', 'isFire', 'fire_cat', 'geometry',
        'poly_IncidentName', 'poly_GISAcres', 'attr_FireCause', 'attr_POOState',
        'attr_POOCounty', 'attr_FireDiscoveryDateTime', 'attr_FireOutDateTime',
        'in_named_fire',
    ]]
    joined = gpd.sjoin(gdf, ca_counties, how='left', predicate='within')
    county_counts = (
        joined.groupby('name', dropna=True)['fire_cat']
        .sum()
        .reset_index(name='fire_score')
        .sort_values('fire_score', ascending=False)
    )

    fig = px.choropleth_map(
        county_counts,
        geojson=ca_geojson,
        locations='name',
        featureidkey='properties.name',
        color='fire_score',
        color_continuous_scale='YlOrRd',
        map_style='dark',
        zoom=4.5,
        center={'lat': CENTER_LAT, 'lon': CENTER_LON},
        opacity=0.7,
        labels={'fire_score': 'Fire activity score'},
        title='Fire activity score by county (weighted by fire category)',
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    return fig


def make_bar_fire_event(df_biggest_fire):
    fig = px.bar(
        df_biggest_fire,
        x='label', y='acres',
        color='acres', color_continuous_scale=red_colors,
        labels={'label': 'Fire Event', 'acres': 'Estimated burnt acres'},
        title='Top 10 California Fires in 2025',
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
        textposition='top center',
        textfont=dict(size=10, color='white'),
        customdata=df_biggest_fire[['poly_IncidentName', 'acres']],
        hovertemplate='<b>%{customdata[0]}</b><br>Date: %{x|%Y-%m-%d}<br>Acres: %{customdata[1]:,.0f}<extra></extra>',
    ), secondary_y=True)

    for y, label in [(101, 'Unhealthy for sensitive groups'), (151, 'Unhealthy for all')]:
        fig.add_hline(
            y=y, secondary_y=False,
            line=dict(dash='dash', color=line_reds[-2], width=1.5),
            opacity=0.7,
            annotation_text=label,
            annotation_position='top right',
        )

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

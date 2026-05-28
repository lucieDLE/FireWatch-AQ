"""
Data Cleaning/Exploration figures — not used in the dashboard (yet?).
"""
from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.display import green_colors, red_colors, line_greens, line_reds, FIRE_CAT_NAMES


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
            fillcolor=green_colors[idx + 1],
            line=dict(color=line_greens[idx + 1]),
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
                fillcolor=red_colors[idx + 1],
                line=dict(color=line_reds[idx + 1]),
                marker_size=3, line_width=1,
                jitter=1.0, whiskerwidth=0.2,
            ), row=1, col=idx + 1)

    fig.update_traces(showlegend=False)

    for idx, name in enumerate(FIRE_CAT_NAMES):
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=12, color=green_colors[idx + 1], symbol='square',
                        line_width=1, line_color=line_greens[idx + 1]),
            name=name,
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

    for label, mask, color in [
        ('True Fire (isFire=1)',     df['isFire'] == 1, red_colors[-1]),
        ('Misclassified (isFire=0)', df['isFire'] == 0, red_colors[2]),
    ]:
        fig.add_trace(go.Histogram(
            x=df.loc[mask, 'daynight'], name=label,
            marker_color=color, opacity=0.85,
            legend='legend2',
        ), row=1, col=1)

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
        height=450, bargap=0.2,
        yaxis_title='Number of pixels',
        legend =dict(orientation='h', x=0.90, y=1.30, xanchor='left', bgcolor='rgba(0,0,0,0)'),
        legend2=dict(orientation='h', yanchor='bottom', xanchor='left',   y=-0.25, x=0,
                     bgcolor='rgba(0,0,0,0.3)', borderwidth=0),
        legend3=dict(orientation='h', yanchor='bottom', xanchor='center', y=-0.25, x=0.5,
                     bgcolor='rgba(0,0,0,0.3)', borderwidth=0),
        legend4=dict(orientation='h', yanchor='bottom', xanchor='left',   y=-0.25, x=0.7,
                     bgcolor='rgba(0,0,0,0.3)', borderwidth=0),
    )
    return fig


def make_scan_track_distribution(df):
    fig = go.Figure([
        go.Histogram(x=df['scan'],  name='scan',  marker_color=red_colors[2],  opacity=.8),
        go.Histogram(x=df['track'], name='track', marker_color=red_colors[-1], opacity=.8),
    ])
    fig.add_vline(x=0.6, line_width=3, line_dash='dash',
                  line_color=line_reds[-1], annotation_text='threshold')
    fig.update_layout(
        template='plotly_dark',
        title_text='Scan and Track distribution',
        bargap=0.3, bargroupgap=0,
    )
    fig.update_yaxes(title_text='Number of pixels')
    fig.update_xaxes(title_text='pixel size')
    return fig

import path_setup  # noqa: F401

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from src.config import POLLUTANT_THRESHOLDS
from src.display import green_colors, red_colors, line_greens, line_reds, MARGIN, TITLE_DICT, LEGEND_BOTTOM
import numpy as np


def make_pollutant_distribution(df):
    fig = px.histogram(df, x="State Name", color='Parameter Name', color_discrete_sequence=red_colors[::-1])
    fig.update_layout(
        template='plotly_dark',
        barmode='stack',
        xaxis={'categoryorder': 'total descending'},
        title=dict(text='Pollutant Distribution across states',),
        legend={**LEGEND_BOTTOM, 'title_text': '', 'y':1.0},
        margin=MARGIN
    )
    fig.update_xaxes(title_text='', tickangle=45, automargin=True, tickfont=dict(size=10))
    return fig


def make_aq_us_plot(df_county, list_best=['WA', 'ID', 'MS'], list_worst=['CA', 'TX', 'AZ']):
    df_no_exceed = df_county.loc[df_county['primary_exceedance'] == 0]
    df_exceed = df_county.loc[df_county['primary_exceedance'] > 0]

    df_no_exceed = df_no_exceed.loc[df_no_exceed['observation'] > 1000]
    df_exceed = df_exceed.loc[df_exceed['primary_exceedance'] > 5]

    sizeref = 2. * df_county['primary_exceedance'].max() / (22 ** 2)
    sizeref_2 = 2. * df_no_exceed['observation'].max() / (22 ** 2)

    fig = go.Figure()

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

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        name='Worst states (CA, TX, AZ)',
        marker=dict(symbol='square', size=12, color='rgba(120,70,150,0.)',
                    line=dict(color=line_reds[-2], width=1.5)),
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        name='Best states (WA, ID, MS)',
        marker=dict(symbol='square', size=12, color='rgba(120,70,150,0.)',
                    line=dict(color=line_greens[-2], width=1.5)),
    ))

    fig.update_layout(
        template='plotly_dark',
        title=dict(
            text='County-level Pollutant Exceedances<br>(Click legend to toggle traces)',
            **TITLE_DICT
        ),
        showlegend=True,
        legend=LEGEND_BOTTOM,
        geo=dict(
            scope='usa',
            subunitcolor='rgb(100,100,100)',
        ),
        margin=MARGIN,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


def compute_max_boxplot(df_stats, states_list, n_cols=3):
    custom_colors = green_colors[0:3] + red_colors[0:3]
    custom_lines  = line_greens[0:3] + line_reds[0:3]

    pollutants_list = df_stats['Parameter Name'].unique()
    n_rows = int(np.ceil(len(pollutants_list) / n_cols))
    v_space = min(0.06, 0.15 / (n_rows - 1)) if n_rows > 1 else 0.0

    fig = make_subplots(
        rows=n_rows, cols=n_cols,
        subplot_titles=pollutants_list,
        vertical_spacing=v_space,
        horizontal_spacing=0.05,
    )

    for plot_idx, pollutant in enumerate(pollutants_list):
        row = plot_idx // n_cols + 1
        col = plot_idx % n_cols + 1
        col_idx = plot_idx  # legend shown only for the first subplot
        for idx, state_name in enumerate(states_list):
            df_ca_pm = df_stats.loc[
                (df_stats['State Name'] == state_name) &
                (df_stats['Parameter Name'] == pollutant)
            ]
            df_maxes = df_ca_pm[['1st Max Value', '2nd Max Value', '3rd Max Value', '4th Max Value']]
            np_maxes = df_maxes.to_numpy().reshape(-1)

            if len(np_maxes) > 5:
                fig.add_trace(go.Box(
                    y=np_maxes,
                    name=state_name,
                    showlegend=(col_idx == 0),
                    fillcolor=custom_colors[idx],
                    line=dict(color=custom_lines[idx]),
                    marker_size=3, line_width=1,
                    whiskerwidth=0.5,
                ), row=row, col=col)
            else:
                fig.add_trace(go.Box(
                    y=np_maxes,
                    name=state_name,
                    boxpoints='all',
                    showlegend=(col_idx == 0),
                    fillcolor='rgba(255,255,255,0)',
                    line=dict(color='rgba(255,255,255,0)'),
                    marker_size=3, line_width=1,
                    marker=dict(color=custom_lines[idx]),
                ), row=row, col=col)

        fig.add_hline(
            y=POLLUTANT_THRESHOLDS[pollutant][0],
            line_width=2, line_dash='dash',
            line_color=red_colors[-1],
            showlegend=(col_idx == 0),
            opacity=0.8,
            name='guideline threshold',
            annotation_text=f'{POLLUTANT_THRESHOLDS[pollutant][0]} {POLLUTANT_THRESHOLDS[pollutant][1]}',
            annotation_position='top left',
            row=row, col=col,
        )

    fig.update_layout(
        template='plotly_dark',
        title_text='Pollutant distribution by state',
        legend=LEGEND_BOTTOM,
        margin=dict(l=10, r=10, t=55, b=60),
    )
    fig.update_xaxes(showticklabels=False)
    return fig

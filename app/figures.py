import pandas as pd 
import plotly.graph_objects  as go
from plotly.subplots import make_subplots

line_colors = ['rgba(250,140,85,1.0)', 'rgba(250,140,85,1.0)', 'rgba(227,74,51,1.0)', 'rgba(179,0,0,1.0)', 'rgba(100,0,0,1.0)']

colors_full = ['rgba(254,240,217,0.8)', 'rgba(253,204,138,0.8)', 'rgba(252,141,89,0.8)', 'rgba(227,74,51,0.8)', 'rgba(179,0,0,0.8)', ]
colors_light = ['rgba(254,240,217,0.4)', 'rgba(253,204,138,0.4)', 'rgba(252,141,89,0.4)', 'rgba(227,74,51,0.4)', 'rgba(179,0,0,0.4)', ]

names = ["Very Small", "Small", "Medium", "Large", "Extreme"]
legend = [
    "Very Small: (≤5 MW)",
    "Small: (5-25 MW)",
    "Medium: (25-100 MW)",
    "Large: (100-500 MW)",
    "Extreme: (>500 MW)",
  ]


def make_fire_category_repartition(df, df_cleaned):

    fig = make_subplots(
        rows=1, cols=5,
        column_widths=[0.2, 0.2, 0.2, 0.2, 0.2],
        subplot_titles=names,
        shared_yaxes=False,
    )

    for idx in range(len(names)):
        df_cat = df.loc[df.fire_cat == idx]

        fig.add_trace(go.Box(
            y=df_cat['frp'],
            name='Raw',
            legendgroup='Raw',
            showlegend=(idx == 0),
            fillcolor=colors_light[idx],
            line=dict(color=line_colors[idx]),

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
                fillcolor=colors_full[idx],
                line=dict(color=line_colors[idx]),

                marker_size=3, line_width=1,
                jitter=1.0, whiskerwidth=0.2,
            ), row=1, col=idx + 1,)
        

    fig.update_traces(showlegend=False) # remove the clean and raw


    # add custom legend
    for idx, legend_category in enumerate(legend):
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=12, color=colors_full[idx], symbol='square', line_width=1, line_color=line_colors[idx]),
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
        ('True Fire (isFire=1)',      df['isFire'] == 1, colors_full[3]),
        ('Misclassified (isFire=0)',  df['isFire'] == 0, colors_full[1]),
    ]:
        fig.add_trace(go.Histogram(
            x=df.loc[mask, 'daynight'], name=label,
            marker_color=color, opacity=0.85,
            legend='legend2',
        ), row=1, col=1)

    # Panel 2 — Types (numeric x so bars land at 0/1/2/3)
    for type_val, label, color in [
        (0, '0: Vegetation Fire', colors_full[3]),
        (1, '1: Volcano',         colors_full[1]),
        (2, '2: Static',          colors_full[1]),
        (3, '3: Offshore',        colors_full[1]),
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
        ('l', 'l: low confidence',     colors_full[1]),
        ('n', 'n: nominal confidence', colors_full[3]),
        ('h', 'h: high confidence',    colors_full[3]),
    ]:
        fig.add_trace(go.Histogram(
            x=df.loc[df['confidence'] == conf_val, 'confidence'], name=label,
            marker_color=color, opacity=0.85,
            legend='legend4',
        ), row=1, col=3)

    # Global top legend — Kept vs Removed
    for label, color in [('Kept in dataset', colors_full[3]), ('Removed from dataset', colors_full[1])]:
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
        go.Histogram(x=df["scan"], name='scan', marker_color=colors_full[2], opacity=0.8),
        go.Histogram(x=df["track"], name='track', marker_color=colors_full[3], opacity=0.8),
        ],)

    fig.add_vline(x=0.6, line_width=3, line_dash="dash", line_color=line_colors[3], annotation_text='threshold')
    fig.update_layout(
        template='plotly_dark',
        title_text='Scan and Track distribution',
        bargap=0.3, # gap between bars of adjacent location coordinates
        bargroupgap=0, # gap between bars of the same location coordinates

)
    fig.update_yaxes(title_text='Number of pixels')
    fig.update_xaxes(title_text='pixel size')

    return fig

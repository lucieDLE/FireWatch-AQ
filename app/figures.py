import pandas as pd 
import plotly.graph_objects  as go
from plotly.subplots import make_subplots
import plotly.express as px
# made from :
# from https://colorbrewer2.org/

green_colors = [
"#c7e9c0",
"#a1d99b",
"#74c476",
"#41ab5d",
"#238b45",
"#005a32",
    ]
line_greens = [
"#a1d99b",
"#74c476",
"#41ab5d",
"#238b45",
"#005a32",
"#00441b"
    ]

line_reds = [
    'rgba(250,140,85,1.0)',
    'rgba(250,140,85,1.0)',
    'rgba(250,100,70,1.0)',
    'rgba(227,74,51,1.0)',
    'rgba(179,0,0,1.0)',
    'rgba(100,0,0,1.0)'
    ]

red_colors = [
    'rgba(254,240,217,0.8)',
    'rgba(253,204,138,0.8)',
    'rgba(253,187,132,0.8)',
    'rgba(252,141,89,0.8)',
    'rgba(227,74,51,0.8)',
    'rgba(179,0,0,0.8)', 
    ]


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
            x=.75,
            y=.5,
            xanchor='right',
        ),
        geo=dict(
            scope='usa',
            subunitcolor='rgb(100,100,100)',
            domain=dict(x=[0, 1], y=[0, 1]),
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_xaxes()
    return fig


def compute_max_boxplot(df_stats, states_list):

    custom_colors = green_colors[0:3] + red_colors[0:3]
    custom_lines  = line_greens[0:3] + line_reds[0:3]

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
    )
    fig.update_xaxes(showticklabels=False)
    return fig
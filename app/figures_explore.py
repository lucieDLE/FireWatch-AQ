"""
Data Cleaning/Exploration figures — not used in the dashboard (yet?).
"""
from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from display import green_colors, red_colors, line_greens, line_reds, FIRE_CAT_NAMES


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




def make_pollutant_number_pie_chart(df_aqi):
    df_pollutant_counts = df_aqi['n_pollutants'].value_counts().to_frame().reset_index()
    
    fig = go.Figure([go.Pie(
            labels=df_pollutant_counts['n_pollutants'], 
            values=df_pollutant_counts['count'],
            pull=[0.1, 0, 0, 0],
            name='Number of pollutants per monitor'
        )])
    fig.update_traces(
        textinfo='text+percent+label', 
        marker=dict(colors=green_colors[::-1], line=dict(color=line_greens[-1], width=1)))

    fig.update_layout(
        
        margin = dict(t=40, l=0, r=0, b=0) ,
        # title_text="Number of pollutant per monitor",
        legend=dict(
                xanchor='right', y=.5, x=.75,
                title='Number of pollutants'
            ),
        )

    return fig


def make_wrong_guidance_plot(df_aqi):
    indices = [
        "Unhealthy -> Very Unhealthy",
        "Unhealthy for SG -> Unhealthy" ,
        "Moderate -> Unhealthy for SG", 
        "Healthy -> Moderate", 
    ]

    values = []
    for threshold in [200, 150, 100, 50]:
        df_threshold = df_aqi.loc[ (df_aqi['max_AQI'] <= threshold) & (df_aqi['composite_penalty'] > threshold) ]
        values.append(len(df_threshold))

    colors = [green_colors[-2], red_colors[-2], red_colors[-2] , red_colors[-3]]

    fig = go.Figure(go.Bar(
            x=values,
            y=indices,
            orientation='h',
            marker_color=colors
        ))

    fig.update_layout(
        xaxis=dict( showgrid=False, 
                    title='Days where sum_AQI pushes a site into a higher EPA health category than max_AQI',
                    ),
        title='How many days were people given wrong health guidance?',
        plot_bgcolor='white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
    )

    return fig




def make_barplot_sum_aqi(df_aqi):

    AQI_BANDS_COLOR = [ (0,   50,  line_greens[-2]), (51,  100, '#FFBF00'), (101, 150, '#EB6F2B'),
                        (151, 200, line_reds[-2]), (201, 300, '#6C3082'), (301, 400, '#58111A'),]


    def attribute_color_to_val(row):
        for aqi_band in AQI_BANDS_COLOR:
            if aqi_band[0] <= row['AQI'] <= aqi_band[1]:
                return aqi_band[2].replace('0.3', '0.5')



    df_threshold = df_aqi.loc[ (df_aqi['max_AQI'] <=150) & (df_aqi['sum_AQI'] > 150) ]
    df_threshold = df_threshold.loc[ df_threshold['n_pollutants'] == 4]

    row = df_threshold.sort_values(by='hidden_pollution', ascending=False).iloc[4]

    indices =['Daily AQI Value_PM2.5', 'Daily AQI Value_PM10' , 'Daily AQI Value_O3', 'Daily AQI Value_NO2']


    small_df = pd.DataFrame(data= {
        'pollutant': ['PM2.5', 'PM10', 'O3', 'NO2'],
        'AQI':row[indices].to_list(),
        })

    small_df['color'] = small_df.apply(lambda row: attribute_color_to_val(row), axis=1)


    small_df_sorted = small_df.sort_values(by='AQI', ascending=False).reset_index()
    values = (small_df_sorted['AQI'] - 50.).clip(0)
    list_values = values.to_list()
    list_values[0]+=50


    title_2 = 'Exceedance sum: ' + str(sum(list_values))
    title_1='Air composition and AQI corresponding value'


    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.7, 0.3],
        subplot_titles=[title_1, title_2],
    )



    # ------------------  Figure 1 ----------------
    fig.add_trace(go.Bar(
        x=small_df['AQI'],
        y=small_df['pollutant'],
        orientation='h',
        marker_color=small_df['color'],
        opacity=1,
        showlegend=False,
        ), row=1, col=1
    )

    fig.update_layout(
        xaxis=dict( showgrid=False, ),
        plot_bgcolor='white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
    )
    fig.add_vline(x=50, 
                line_width=2, line_dash='dash',
                line_color='black',
                name='guideline threshold',
                annotation_text=f'Threshold for Good Air (AQI=50)',
                annotation_position='top',row=1, col=1)



    # ------------------  Figure 2 ----------------

    for idx, row in small_df_sorted.iterrows():
        value = list_values[idx]
        text = row['pollutant']
        if idx != 0:
            text = "Excess " + row['pollutant'],


        fig.add_trace(go.Bar(
            name=row['pollutant'], 
            x=['Sum AQI'], 
            y=[value],
            marker_color=red_colors[::-1][idx],
            legend='legend1',
            text=text,
        ), row=1, col=2)

    fig.update_layout(  barmode='stack',
                        legend1=dict(
                            orientation='v',
                            yanchor='bottom', 
                            xanchor='right',   
                            y=.5, 
                            x=1.05,),
                        margin = dict(t=100, l=0, r=30, b=0) ,

    )
    fig.layout.annotations[0].update(y=1.15)  # left title
    fig.layout.annotations[1].update(y=1.15)  # right title

    return fig
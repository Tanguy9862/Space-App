import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from assets.data.data_processing import df

FORMATS = ["%a %b %d, %Y", "%a %b %d, %Y %H:%M UTC", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S"]
BG_TRANSPARENT = 'rgba(0,0,0,0)'
WITHOUT_PADDING = dict(pad=15, t=0, b=0, l=0, r=0)
HOVERLABEL_TEMPLATE = dict(
    bgcolor='rgba(11, 6, 81, 0.8)',
    bordercolor='rgba(11, 6, 81, 0.8)',
    font=dict(
        color='white'
    )
)

# df['YEAR_LAUNCH'] = df.Date.str.split(",").str[1].str.strip().str.split(" ").str[0]
df['YEAR_LAUNCH'] = pd.DatetimeIndex(df['Date']).year


## LAUNCH PER YEAR
df_launch_per_year = df.groupby("YEAR_LAUNCH").count()
df_launch_per_year = df_launch_per_year.drop(df_launch_per_year[df_launch_per_year.columns.difference(["Organisation"])], axis=1).rename(columns={'Organisation': 'Count'})

fig_launch_per_year = go.Figure(
    go.Scatter(
        x=df_launch_per_year.index,
        y=df_launch_per_year['Count'],
        name='Launches',
        line=dict(color='rgb(1, 230, 239)', width=2, shape='spline'),
        showlegend=False
    )
)

fig_launch_per_year.update_layout(
    height=300,
    paper_bgcolor=BG_TRANSPARENT,
    plot_bgcolor=BG_TRANSPARENT,
    font=dict(color="white"),
    margin=WITHOUT_PADDING,
    hovermode='x unified',
    hoverlabel=HOVERLABEL_TEMPLATE,
    xaxis=dict(showgrid=False, showspikes=False, tickfont=dict(color='rgba(255, 255, 255, 0.6)')),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
)

fig_launch_per_year.update_traces(
    fill='tozeroy',
    fillcolor='rgba(0 0, 0, 0.3)',
    hovertemplate='%{y}'
)


## BEST MONTHS

# def get_formatted_date(x):
#     if 'UTC' in x:
#         x = x.rsplit(" ", 2)[0]
#         return pd.to_datetime(x, format="%a %b %d, %Y")
#     else:
#         pd.to_datetime(x, format="%a %b %d, %Y")


def convert_to_date(date_str):
    for date_format in FORMATS:
        try:
            return pd.to_datetime(date_str, format=date_format)
        except ValueError:
            pass
    return None


def get_launch_per_month(df, year=None):
    if year:
        new_df = df.query('YEAR_LAUNCH == @year').groupby('MONTH')['TOTAL'].sum().reset_index()
    else:
        new_df = df.groupby('MONTH')['TOTAL'].sum().reset_index()
    new_df['BAR_COLOR'] = 'rgba(255, 255, 255, 0.1)'
    new_df.loc[new_df['TOTAL'] == new_df['TOTAL'].min(), 'BAR_COLOR'] = '#FB7089'
    new_df.loc[new_df['TOTAL'] == new_df['TOTAL'].max(), 'BAR_COLOR'] = '#00ff9f'
    return new_df.sort_values(by='MONTH', key=lambda x: pd.to_datetime(x, format='%B')).iloc[::-1]


df['FORMATTED_DATE'] = df['Date'].apply(lambda x: convert_to_date(x))
df_best_month_launch = df.groupby(['FORMATTED_DATE', 'YEAR_LAUNCH']).size().reset_index(name='TOTAL')
df_best_month_launch['MONTH'] = df_best_month_launch['FORMATTED_DATE'].dt.strftime('%B')
df_monthly = get_launch_per_month(df_best_month_launch)

fig_monthly = px.bar(
    df_monthly,
    x="TOTAL",
    y='MONTH',
    height=300,
)

fig_monthly.update_traces(
    hovertemplate=None,
    width=0.1,
    marker_color=df_monthly['BAR_COLOR'],
    marker_line_color=df_monthly['BAR_COLOR']
)

fig_monthly.update_layout(
    paper_bgcolor=BG_TRANSPARENT,
    plot_bgcolor=BG_TRANSPARENT,
    margin=WITHOUT_PADDING,
    hoverlabel=HOVERLABEL_TEMPLATE,
    hovermode='y unified',
    coloraxis_showscale=False,
    yaxis=dict(title=None, showgrid=False, zeroline=False, showspikes=False, color='white'),
    xaxis=dict(showgrid=False, zeroline=False, visible=False, tickprefix='Launches : ')
)

## SUNBURST


def filter_sunburst_year(df, year):
    return df.query('YEAR_LAUNCH == @year')


def plot_sunburst(df):
    fig = px.sunburst(
        df,
        path=['Country', 'Organisation', 'Mission_Status'],
        height=300,
        maxdepth=2
    )

    fig.update_traces(
        marker_colors=df_sunburst['SUNBURST_COLOR'],
        marker_line=dict(color='rgba(255, 255, 255, 0.2)', width=2),
        insidetextfont=dict(color="white"),
        hovertemplate=(
            '<b>%{parent}</b><br>'
            '%{label} : %{value}<br>'
        )
    )

    fig.update_layout(
        paper_bgcolor=BG_TRANSPARENT,
        margin=WITHOUT_PADDING,
        hoverlabel=HOVERLABEL_TEMPLATE
    )
    return fig


df_sunburst = df
df_sunburst['SUNBURST_COLOR'] = 'rgba(0, 0, 0, 0.3)'
sunburst_fig = plot_sunburst(df_sunburst)



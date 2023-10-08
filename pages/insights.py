import dash
import dash_mantine_components as dmc
from dash import dcc, callback, Input, Output, ctx, Patch, clientside_callback
from utils.data_processing import df
from utils.insights_processing import fig_launch_per_year, fig_monthly, df_best_month_launch, get_launch_per_month, \
    sunburst_fig, df_sunburst, filter_sunburst_year, plot_sunburst
from dash_iconify import DashIconify
from numpy import isnan
import plotly.graph_objects as go
import json
import datetime as dt

now = dt.datetime.now()
DATE_UPDATE = now.strftime('%Y-%m-%d %H:%M')

FIG_CONFIG = {
    'displayModeBar': False,
    'scrollZoom': False,
    'showTips': False
}

with open('data/next_launch_data.json', 'r', encoding='utf-8') as json_file:
    next_launch_data = json.load(json_file)

dash.register_page(__name__, title='Space Exploration | Insights')


def right_content_next_launch(rocket_name, mission_description, live_link):
    return [
        dmc.Title(rocket_name, order=3, color='white', align='center'),
        dmc.Spoiler(
            showLabel='Show more..',
            hideLabel='Hide',
            maxHeight=95,
            style={'text-align': 'center'},
            children=[
                dmc.Text(mission_description, color='white', align='center')
            ]
        ),
        *[
            dmc.Anchor(
                [
                    dmc.Button(
                        'live',
                        uppercase=True,
                        variant='transparent',
                        color='grape',
                        size='lg',
                        leftIcon=DashIconify(icon='solar:play-line-duotone'),
                        mt=25,
                    )
                ],
                href=live_link
            )
            if live_link else None
        ]

    ]


def right_content_on_year(most_used_model, organisation, model_launches, year):
    return [
        dmc.Grid(
            [
                dmc.Col([dmc.Title(most_used_model, order=3, color='white', align='center')], span=12),
                dmc.Col(
                    [
                        dmc.Text(
                            [
                                f'The most frequently launched rocket model in the year {year} is '
                                f'{most_used_model} ({organisation}), with a total of {model_launches} launches.'
                            ],
                            color='white', align='center'
                        )
                    ],
                    span=12
                )
            ]
        )
    ]


def right_content(general_data, title, add_content_fn, image=None, *args, **kwargs):
    return [
        dmc.Title(title, color='white'),
        dmc.Group(
            [
                *[dmc.FloatingTooltip(
                    label=values[0],
                    children=[
                        dmc.Stack(
                            [
                                dmc.Text(features, color='rgba(255, 255, 255, 0.4)', style={'font-size': '1rem'}),
                                dmc.Title(values[1], color='white', order=4)

                            ],
                            align='center',
                            spacing=10
                        )
                    ]
                )
                    for features, values in general_data.items()],
                *[
                    dmc.Col(
                        [
                            dmc.Image(
                                src=image,
                                mt=25,
                                mb=15,
                                radius=4,
                                withPlaceholder=True,
                                style={
                                    'width': '65%',
                                    'display': 'block',
                                    'margin-left': 'auto',
                                    'margin-right': 'auto'
                                },
                                styles={
                                    'placeholder': {'background-color': '#000000'}
                                }
                            )
                        ], span=12
                    )
                ],
                *add_content_fn(*args, **kwargs)

            ],
            mt=25,
            position='center'
        )
    ]


def get_highest_values(df, target):
    new_df = df.groupby(target).size().reset_index(name='Count')
    return new_df.loc[new_df.Count.idxmax(), target]


layout = dmc.NotificationsProvider(
    [
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Container(
                            [
                                dmc.Group(
                                    [
                                        *[
                                            dmc.Stack(
                                                [
                                                    dmc.Text(key, transform='uppercase',
                                                             color='rgba(255, 255, 255, 0.4)',
                                                             style={'font-size': '1rem'}),
                                                    dmc.Title(value, color='white', order=4)
                                                ],
                                                spacing=0
                                            )
                                            for key, value in next_launch_data[0].items() if
                                            key in {'NEXT LAUNCH', 'ORGANISATION',
                                                    'ROCKET'}
                                        ],
                                        *[
                                            dmc.Tooltip(
                                                [
                                                    dmc.ActionIcon(
                                                        DashIconify(icon='ri:more-fill', color='white'),
                                                        id='next-launch-btn',
                                                        variant='outline',
                                                        radius='lg'
                                                    )
                                                ],
                                                label='View upcoming rocket launch details',
                                                withArrow=True,
                                                transition='fade'
                                            )

                                        ]
                                    ],
                                    position='apart',
                                    mb='lg'
                                ),
                                dmc.Divider(labelPosition='center', label='Launches over time', color='white', mt=35,
                                            mb=20),
                                dmc.Group(
                                    [

                                        dmc.ActionIcon(
                                            DashIconify(icon='iconoir:rocket', width=20),
                                            id='success',
                                            size='lg',
                                            color='green',
                                            variant='outline',
                                            radius='lg'
                                        ),
                                        dmc.ActionIcon(
                                            DashIconify(icon='tabler:rocket-off', width=20),
                                            id='failure',
                                            size='lg',
                                            color='red',
                                            variant='outline',
                                            radius='lg'
                                        ),
                                        dmc.Tooltip(
                                            [
                                                dmc.ActionIcon(
                                                    [
                                                        DashIconify(icon='ic:baseline-restore', width=20),
                                                    ],
                                                    id='monthly-restore',
                                                    variant='outline',
                                                    size="lg",
                                                    radius='lg'
                                                ),
                                            ],
                                            label='Reset to include all Years',
                                            withArrow=True,
                                            transition='fade'
                                        )
                                    ],
                                    mt=15,
                                    position='center'
                                ),
                                dcc.Graph(
                                    id='launches-fig',
                                    figure=fig_launch_per_year,
                                    config=FIG_CONFIG
                                ),
                            ],
                            px=0,
                            style={
                                'background-color': 'rgba(0,0,0,0)',
                                'width': '85%',
                            }
                        ),
                        dmc.Container(
                            [
                                dmc.Grid(
                                    [
                                        dmc.Col(
                                            [
                                                dcc.Graph(id='monthly-launches-fig', figure=fig_monthly,
                                                          config=FIG_CONFIG)
                                            ],
                                            lg=6, md=12
                                        ),
                                        dmc.Col(
                                            [
                                                dcc.Graph(id='sunburst-fig', figure=sunburst_fig, config=FIG_CONFIG)
                                            ],
                                            offsetLg=2,
                                            lg=4, md=12
                                        )
                                    ],
                                    mt=35
                                )

                            ],
                            p=0,
                            style={'width': '85%'},
                            mt='lg',
                            mb=25
                        )
                    ],
                    mt=70,
                    md=12,
                    lg=8,
                ),
                dmc.Col(
                    [
                        dmc.Stack(
                            id='right-content',
                            align='center',
                            mb=25
                        )
                    ],
                    offsetLg=1,
                    offsetMd=0,
                    mt=70,
                    md=12,
                    lg=3
                ),
                dmc.Col(
                    [
                        dmc.Container(id='notifications-container')
                    ]
                )
            ],
        )
    ]
)


@callback(
    Output('right-content', 'children'),
    Output('right-content', 'className'),
    Input('launches-fig', 'clickData'),
    Input('next-launch-btn', 'n_clicks'),
    prevent_initial_call=True
)
def update_right_content(data, _):
    input_id = ctx.triggered_id

    if input_id == 'launches-fig':
        general_data = dict()
        year = data['points'][0]['x']
        df_year = df.query('YEAR_LAUNCH == @year').copy()
        general_data['Avg'] = [
            'Average price per rocket',
            f'${df_year["Price"].mean().round(1)}M' if not isnan(df_year["Price"].mean()) else "-"
        ]
        general_data['Country'], general_data['Organisation'] = [
            [f'{col} with the most launches'] + [get_highest_values(df_year, target=col)]
            for col in ['Country', 'Organisation']
        ]

        # Get the most used rocket model in the selected year
        df_year['Rocket_Model'] = df_year['Detail'].str.split('|').str[0].str.strip()
        df_year['Rocket_Model'] = df_year['Rocket_Model'].str.replace(r' \(.*\)', '', regex=True).str.strip()
        df_year['Rocket_Model'] = df_year['Rocket_Model'].apply(lambda x: x.split('/')[0] if '/' in x else x)
        most_used_model = df_year.groupby(['Rocket_Model', 'Organisation']).agg(
            {'Detail': 'count', 'Image_Link': 'first'}).reset_index()
        most_used_model = most_used_model.sort_values('Detail', ascending=False).iloc[0]

        return right_content(
            general_data,
            title=year,
            add_content_fn=right_content_on_year,
            image=most_used_model['Image_Link'],
            most_used_model=most_used_model['Rocket_Model'],
            organisation=most_used_model['Organisation'],
            model_launches=most_used_model['Detail'],
            year=year
        ), 'hide'

    else:
        branch = next_launch_data[0]
        organisation = branch['ORGANISATION']
        year = dt.datetime.now().year

        next_launch_general = {
            'PRICE': ['Rocket price in millions of dollars', (branch['PRICE'] and f'${branch["PRICE"]}M') or '-'],
            'TOTAL MISSION': [f'Total mission of {organisation}', branch['TOTAL MISSION'] or '-'],
            f'IN {year}': [f'Total mission of {organisation} in {year}', branch['TOTAL MISSION YEAR'] or '-']
        }

        return right_content(
            next_launch_general,
            title=organisation,
            image=branch['IMAGE'],
            add_content_fn=right_content_next_launch,
            rocket_name=branch['ROCKET'],
            mission_description=branch['MISSION DETAIL'],
            live_link=branch['VIDEO']
        ), 'hide'


clientside_callback(
    """
    function(className) {
        return "fade-in";
    }
    """,
    Output('right-content', 'className', allow_duplicate=True),
    Input('right-content', 'className'),
    prevent_initial_call=True
)


@callback(
    Output('launches-fig', 'figure'),
    Input('failure', 'n_clicks'),
    Input('success', 'n_clicks'),
)
def update_launch_year_plot(_1, _2):
    input_id = ctx.triggered_id and ctx.triggered_id.title()

    if input_id:
        index = 0 if input_id == 'Failure' else 1
        n = ctx.args_grouping[index]['value']
        if n % 2:
            status_df = df.groupby(["YEAR_LAUNCH", "Mission_Status_Binary"]).size().reset_index(name='Total')
            status_df = status_df.query('Mission_Status_Binary == @input_id')

            fig_launch_per_year.add_trace(
                go.Scatter(
                    x=status_df['YEAR_LAUNCH'],
                    y=status_df['Total'],
                    mode='lines',
                    line=dict(color='#00ff9f' if index else '#FB7089', dash='dot'),
                    showlegend=False,
                    name=input_id
                )
            )
        else:
            fig_launch_per_year.data = tuple(trace for trace in fig_launch_per_year.data if trace['name'] != input_id)

        return fig_launch_per_year

    fig_launch_per_year.data = fig_launch_per_year.data[:1]

    return fig_launch_per_year


@callback(
    Output('monthly-launches-fig', 'figure'),
    Output('sunburst-fig', 'figure'),
    Input('launches-fig', 'clickData'),
    Input('monthly-restore', 'n_clicks'),
    prevent_initial_call=True
)
def update_monthly_plot(data, _):
    input_id = ctx.triggered_id

    if input_id == 'launches-fig':
        year = data['points'][0]['x']
        filtered_monthly_df = get_launch_per_month(df_best_month_launch, year)

        patched_monthly_figure = Patch()
        patched_monthly_figure['data'][0]['x'] = filtered_monthly_df['TOTAL']
        patched_monthly_figure['data'][0]['y'] = filtered_monthly_df['MONTH']
        patched_monthly_figure['data'][0]['marker']['color'] = filtered_monthly_df['BAR_COLOR']
        patched_monthly_figure['data'][0]['marker']['line']['color'] = filtered_monthly_df['BAR_COLOR']
        # patched_monthly_figure['layout']['yaxis']['ticksuffix'] = f' (in {year})'

        filtered_sunburst_df = filter_sunburst_year(df_sunburst, year)
        updated_sunburst = plot_sunburst(filtered_sunburst_df)

        return patched_monthly_figure, updated_sunburst
    else:
        return fig_monthly, sunburst_fig


@callback(
    Output('notifications-container', 'children'),
    Input('notifications-container', 'children')
)
def show_notifications(_):
    return [
        dmc.Notification(
            id='notif',
            title='Data Last Updated',
            action='show',
            message=f'Last updated on {DATE_UPDATE}',
            autoClose=False,
            icon=DashIconify(icon='material-symbols:system-update-alt'),
            style={'background-color': 'rgba(0, 0, 0, 0)', 'border': 'none', 'color': 'white'},
            styles={
                'title': {'color': 'white'},
                'description': {'color': '#E6E6E6'}
            }

        ),
    ]

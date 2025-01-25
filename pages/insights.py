import dash
import dash_mantine_components as dmc
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, callback, Input, Output, ctx, Patch, clientside_callback, State
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from numpy import isnan
from plotly.graph_objs import Figure
from utils.insights_processing import plot_launch_per_year, create_df_best_month_launches, create_monthly_bar_chart, \
    create_sunburst_chart
from utils.helpers import create_notification
from collections import deque

FIG_CONFIG = {
    'displayModeBar': False,
    'scrollZoom': False,
    'showTips': False
}

HIDE = {'display': 'none'}

dash.register_page(
    __name__,
    image='insights.png',
    title='Space Exploration | Insights',
    description='Get real-time analytics on space launches. Interactive dashboards allow you to filter by year, '
                'providing insights into launch success rates, most active organizations, and more'
)


def right_content_on_launch(rocket_name, mission_description, live_link):
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
                                    'placeholder': {'background-color': '#000000'},
                                    'image': {'border-radius': '50%', 'object-fit': 'cover'}
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


def add_loading_overlay(elements):
    return [
        dmc.LoadingOverlay(
            children=elements,
            loaderProps={'color': 'white', 'variant': 'dots'},
            overlayColor='#0B0653',
            overlayOpacity=0.4,
            radius=6,
        )
    ]


def get_highest_values(df, target):
    new_df = df.groupby(target).size().reset_index(name='Count')
    return new_df.loc[new_df.Count.idxmax(), target]


layout = dmc.NotificationsProvider(
    [
        dmc.Grid(
            [
                html.Div(id='insights-notifications-container'),
                dcc.Store('next-launch-data'),
                dcc.Store(id='next-launch-last-update'),
                dmc.Col(
                    [
                        dmc.Container(
                            [
                                dmc.Group(
                                    [
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
                                    ],
                                    id='next-launch-container',
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
                                                    id='restore-data',
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
                                dmc.Container(
                                    id='launches-fig-container',
                                    px=0,
                                    children=[
                                        dmc.Center(
                                            [
                                                dmc.Loader(
                                                    color="blue",
                                                    size="md",
                                                    variant="oval",
                                                    mt=250
                                                ),
                                            ]
                                        ),
                                        dcc.Graph(id='launches-fig', style=HIDE)
                                    ]
                                )
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
                                                dcc.Graph(id='bar-fig', style=HIDE)
                                            ],
                                            lg=6, md=12
                                        ),
                                        dmc.Col(
                                            [
                                                dcc.Graph(id='sunburst-fig', style=HIDE)
                                            ],
                                            offsetLg=2,
                                            lg=4, md=12
                                        )
                                    ],
                                    id='secondary-figures-container',
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
                    add_loading_overlay(
                        [
                            dmc.Stack(
                                id='right-content',
                                align='center',
                            )
                        ]
                    ),
                    offsetLg=1,
                    offsetMd=0,
                    mt=70,
                    md=12,
                    lg=3
                ),
            ],
        )
    ]
)


@callback(
    Output('launches-fig-container', 'children'),
    Input('past-launches-data', 'data'),
)
def create_launches_fig(past_launch_data):
    """
    Plot year launches
    """

    if not past_launch_data:
        return dash.no_update

    df = pd.DataFrame(past_launch_data)
    fig_launch_per_year = plot_launch_per_year(df)

    return add_loading_overlay(
        [
            dcc.Graph(
                id='launches-fig',
                config=FIG_CONFIG,
                figure=fig_launch_per_year,
            )
        ]
    )


@callback(
    Output('launches-fig', 'figure'),
    Input('failure', 'n_clicks'),
    Input('success', 'n_clicks'),
    State('launches-fig', 'figure'),
    State('past-launches-data', 'data'),
    prevent_initial_call=True
)
def launches_add_lines(_1, _2, fig, data):
    """
    Add lines successes and fails on year launches plot
    """
    fig_launch_per_year = Figure(fig)
    df_past_launches = pd.DataFrame(data)
    input_id = ctx.triggered_id and ctx.triggered_id.title()

    if input_id:
        index = 0 if input_id == 'Failure' else 1
        n = ctx.args_grouping[index]['value']
        if n % 2:
            status_df = df_past_launches.groupby(["YEAR_LAUNCH", "Mission_Status_Binary"]).size().reset_index(
                name='Total')
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
    Output('next-launch-container', 'children'),
    Input('next-launch-data', 'data'),
    State('next-launch-container', 'children')
)
def update_next_launch_container(next_launch_info, current_children: list):
    """
    Show details on the right side about next launch
    """
    updated_children = deque(current_children)
    updated_children.extendleft(
        dmc.Stack(
            [
                dmc.Text(key, transform='uppercase',
                         color='rgba(255, 255, 255, 0.4)',
                         style={'font-size': '1rem'}),
                dmc.Title(value, color='white', order=4)
            ],
            spacing=0
        )
        for key, value in next_launch_info[0].items() if
        key in {'NEXT LAUNCH', 'ORGANISATION',
                'ROCKET'}
    )

    return list(updated_children)


@callback(
    Output('right-content', 'children'),
    Output('right-content', 'className'),
    Input('launches-fig', 'clickData'),
    Input('next-launch-btn', 'n_clicks'),
    State('next-launch-data', 'data'),
    State('past-launches-data', 'data'),
    prevent_initial_call=True
)
def update_right_content(click_data, _, next_launch_data, past_launches_data):
    """
    Update right content based on the input triggered (data about past launches or about next launch)
    """
    input_id = ctx.triggered_id

    if input_id == 'launches-fig' and click_data:
        past_launches_data_df = pd.DataFrame(past_launches_data)
        general_data = dict()
        year = click_data['points'][0]['x']
        df_year = past_launches_data_df.query('YEAR_LAUNCH == @year').copy()
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

        pd.set_option('display.max_colwidth', None)
        # print(most_used_model)

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
            add_content_fn=right_content_on_launch,
            rocket_name=branch['ROCKET'],
            mission_description=branch['MISSION DETAIL'],
            live_link=branch['VIDEO']
        ), 'hide'


@callback(
    Output('secondary-figures-container', 'children'),
    Input('past-launches-data', 'data')
)
def create_secondaries_fig(past_launches_data):
    """
    Plot monthly launches(bar chart) and sunburst of organisation/companies/successes vs. fails
    """
    if not past_launches_data:
        return dash.no_update

    past_launches_data_df = pd.DataFrame(past_launches_data)

    return [
        dmc.Col(
            add_loading_overlay(
                dcc.Graph(
                    id='bar-fig',
                    figure=create_monthly_bar_chart(create_df_best_month_launches(past_launches_data_df)),
                    config=FIG_CONFIG
                )
            ),
            lg=6,
            md=12
        ),
        dmc.Col(
            add_loading_overlay(
                dcc.Graph(id='sunburst-fig', figure=create_sunburst_chart(past_launches_data_df), config=FIG_CONFIG)
            ),
            offsetLg=2,
            lg=4,
            md=12
        )
    ]


@callback(
    Output('bar-fig', 'figure'),
    Output('sunburst-fig', 'figure'),
    Input('launches-fig', 'clickData'),
    Input('restore-data', 'n_clicks'),
    State('past-launches-data', 'data'),
    prevent_initial_call=True
)
def update_secondary_figs(click_data, _, past_launches_data):
    """
    Update bar chart and sunburst chart based on year input OR restore input
    """
    input_id = ctx.triggered_id

    if input_id == 'launches-fig' and click_data:
        past_launches_data_df = pd.DataFrame(past_launches_data)
        year = click_data['points'][0]['x']
        filtered_monthly_df = create_df_best_month_launches(past_launches_data_df, year)

        # Update bar chart:
        patched_bar_fig = Patch()
        patched_bar_fig['data'][0]['x'] = filtered_monthly_df['TOTAL']
        patched_bar_fig['data'][0]['y'] = filtered_monthly_df['MONTH']
        patched_bar_fig['data'][0]['marker']['color'] = filtered_monthly_df['BAR_COLOR']
        patched_bar_fig['data'][0]['marker']['line']['color'] = filtered_monthly_df['BAR_COLOR']

        # Update sunburst chart:
        sunburst_fig = create_sunburst_chart(past_launches_data_df, year)

        return patched_bar_fig, sunburst_fig

    elif input_id == 'restore-data':
        past_launches_data_df = pd.DataFrame(past_launches_data)
        return create_monthly_bar_chart(create_df_best_month_launches(past_launches_data_df)), \
            create_sunburst_chart(past_launches_data_df)

    raise PreventUpdate


@callback(
    Output('insights-notifications-container', 'children'),
    Input('next-launch-last-update', 'data'),
    Input('past-launches-last-update', 'data'),
    prevent_initial_call=True
)
def update_insights_notifications(next_launch_update_date, past_launches_update_date):

    next_launch_notification = create_notification(
        page=f'{__name__}-next-launch',
        date=next_launch_update_date,
        data_type='Next Launch',
        freq='every 3 hours',
    )

    past_launches_notification = create_notification(
        page=f'{__name__}-past-launches',
        date=past_launches_update_date,
        data_type='Past Launches',
        freq='every 3 hours',
    )

    return [next_launch_notification, past_launches_notification]



# @callback(
#     Output('notifications-container', 'children'),
#     Input('notifications-container', 'id'),
# )
# def show_notifications(_):
#     return [
#         dmc.Notification(
#             id='notif',
#             title='Data Last Updated',
#             action='show',
#             message=f'Last updated on {read_from_gcs("date_update.txt").download_as_text()}',
#             autoClose=False,
#             icon=DashIconify(icon='material-symbols:system-update-alt'),
#             style={'background-color': 'rgba(0, 0, 0, 0)', 'border': 'none', 'color': 'white'},
#             styles={
#                 'title': {'color': 'white'},
#                 'description': {'color': '#E6E6E6'}
#             }
#         ),
#     ]


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

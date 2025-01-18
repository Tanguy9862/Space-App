import json
import datetime
import dash
import dash_mantine_components as dmc
import dash_extensions as de

from dash import dcc, html, callback, Input, Output, ctx, no_update
from dash_iconify import DashIconify
from random import sample

from utils.cytoscape import nodes_big_dipper, edges_big_dipper, nodes_orion, edges_orion, nodes_scorpion, \
    edges_scorpion, constellation
from utils.helpers import create_notification


LOTTIE_URL = 'https://lottie.host/bd952b99-002b-42d6-875e-57a7924ce27c/pEXSm4MJxX.json'
LOTTIE_OPTIONS = dict(loop=True, autoplay=True)

dash.register_page(
    __name__,
    image='historical.png',
    title='Space Exploration | Historical',
    description='Dive into the key milestones of space exploration, presented in a unique cytoscape constellation '
                'format. Each point represents a significant event, complete with descriptions and images'
)

# with open('data/historical_data.json', 'r', encoding='utf-8') as json_file:
#     historical_data = json.load(json_file)
#
# all_years = [int(item['DATE'].split(',')[-1].strip()) for item in historical_data] + [1950]
# MIN_YEARS, MAX_YEARS = min(all_years), max(all_years)
# YEAR_BOUND_INF, YEAR_BOUND_SUP, YEAR_INCREMENT = 1940, 2021, 20

YEAR_INCREMENT = 20


def right_content(*, date, country, description, image):
    return [
        dmc.Title(date, color='white', align='center'),
        dmc.Container(
            children=[
                dmc.Image(
                    src=image,
                    width='100%',
                    height='100%',
                    # radius=4,
                    withPlaceholder=True,
                    # style={'border-radius': '50%'},
                    styles={
                        # 'placeholder': {'background-color': '#000000'},
                        'image': {'border-radius': '50%', 'object-fit': 'cover'}
                    },
                ) if image else None
            ],
            px=0,
        ),
        dmc.Title(', '.join(country) if isinstance(country, list) else country, order=3, color='white',
                  align='center'),
        dmc.Text([description], color='white', align='center')
    ]


layout = dmc.NotificationsProvider(
    [
        dmc.Grid(
            [
                html.Div(id='historical-notification-container'),
                dcc.Store(id='historical-facts-last-update'),
                dmc.Col(
                    children=[
                        dmc.Container(
                            [
                                de.Lottie(url=LOTTIE_URL, options=LOTTIE_OPTIONS, isClickToPauseDisabled=True)
                            ],
                            className='bg-lottie',
                            px=0,
                            size='80%',
                        ),
                        constellation,
                        dmc.Group(
                            [
                                dmc.RangeSlider(
                                    id='year-slider',
                                    # value=[MIN_YEARS, MAX_YEARS],
                                    # min=MIN_YEARS,
                                    # max=MAX_YEARS,
                                    minRange=1,
                                    # marks=[
                                    #     {'value': i, 'label': i} for i in range(YEAR_BOUND_INF, YEAR_BOUND_SUP, YEAR_INCREMENT)
                                    # ],
                                    color='white',
                                    style={'width': '50%'},
                                    styles={
                                        'bar': {'background-color': '#D291DF', 'height': '3px'},
                                        'track': {'height': '3px'},
                                        'mark': {'display': 'None'},
                                        'markLabel': {'margin-top': '15px'},
                                        'thumb': {'background-color': '#D291DF', 'border': 'solid 2px white'}
                                    }
                                ),
                                dmc.Tooltip(
                                    [
                                        dmc.ActionIcon(
                                            DashIconify(icon='ic:round-refresh', width=25),
                                            id='refresh-btn',
                                            size=30,
                                            style={'background-color': 'rgba(0,0,0,0)'},
                                            color='#00f9ff'
                                        )
                                    ],
                                    label='Display new dates in the constellations',
                                    withArrow=True,
                                    transition='fade'
                                )
                            ],
                            mt=50,
                            mb=50,
                            position='center'
                        ),
                    ],
                    md=12, lg=9
                ),
                dmc.Col(
                    [
                        dmc.Stack(
                            id='historical-content',
                            align='center',
                            justify='center',
                            spacing='25px',
                            style={'height': '100%'},
                            mb=50
                        ),
                    ],
                    md=12, lg=3
                ),
                # dcc.Store(id='historical-data', data=historical_data),
                dcc.Store(id='historical-data', data=None),
            ],
        )
    ],
)


@callback(
    Output('year-slider', 'value'),
    Output('year-slider', 'min'),
    Output('year-slider', 'max'),
    Output('year-slider', 'marks'),
    Input('historical-data', 'data')
)
def update_slider_layout(data):
    all_years = [int(item['DATE'].split(',')[-1].strip()) for item in data] + [1950]
    slider_value = [min(all_years), max(all_years)]
    slider_min, slider_max = slider_value[0], slider_value[1]
    slider_marks = [{'value': i, 'label': i} for i in range(slider_min, slider_max + 1, YEAR_INCREMENT)]

    return slider_value, slider_min, slider_max, slider_marks


@callback(
    Output('cyto-constellation', 'elements'),
    Input('refresh-btn', 'n_clicks'),
    Input('historical-data', 'data'),
    Input('year-slider', 'value'),
    prevent_initial_call=True
)
def update_cytoscape(_, historical_data_gcs, year_range):
    nodes = nodes_big_dipper + nodes_orion + nodes_scorpion
    edges = edges_big_dipper + edges_orion + edges_scorpion

    scaled_data = [item for item in historical_data_gcs if
                   min(year_range) <= int(item['DATE'].split(',')[-1].strip()) <= max(year_range)]

    random_sample = sorted(
        sample(scaled_data, len(nodes) if len(scaled_data) >= len(nodes) else len(scaled_data)),
        key=lambda x: datetime.datetime.strptime(x['DATE'], '%B %d, %Y')
    )

    for idx, node in enumerate(nodes):
        try:
            node['data'] = {**node['data'], **random_sample[idx]}
            node['data']['YEAR'] = node['data']['DATE'].split(',')[-1].strip()
            node['selectable'] = True
        except IndexError:
            for key in node['data']:
                node['data'][key] = None if key != 'id' else node['data'][key]
            node['data']['YEAR'] = ''
            node['selectable'] = False

    return nodes + edges


@callback(
    Output('historical-content', 'children'),
    Output('historical-content', 'className'),
    Input('cyto-constellation', 'tapNodeData'),
    Input('cyto-constellation', 'elements'),
    prevent_initial_call=True
)
def update_historical_content(node_data, all_data):
    input_id = list(ctx.triggered_prop_ids)[0].split('.')[-1]
    if input_id == 'elements':
        return right_content(
            date=all_data[0]['data']['DATE'],
            country=all_data[0]['data']['COUNTRY'],
            description=all_data[0]['data']['DESCRIPTION'],
            image=all_data[0]['data']['IMAGE_LINK'],
        ), 'hide'
    else:
        if not any(node_data[key] for key in node_data if key != 'id'):
            return no_update
        return right_content(
            date=node_data['DATE'],
            country=node_data['COUNTRY'],
            description=node_data['DESCRIPTION'],
            image=node_data['IMAGE_LINK']
        ), 'hide'


@callback(
    Output('historical-content', 'className', allow_duplicate=True),
    Input('historical-content', 'className'),
    prevent_initial_call=True
)
def animation(_):
    return 'fade-in'


@callback(
    Output('historical-notification-container', 'children'),
    Input('historical-facts-last-update', 'data'),
    prevent_initial_call=True
)
def update_notification(last_update):
    return create_notification(
        page=__name__,
        date=last_update,
        data_type='Historical Facts',
        freq='every Monday'
    )

import dash
from dash import dcc, callback, Input, Output, ctx, no_update, clientside_callback
import dash_mantine_components as dmc
import dash_extensions as de
from dash_iconify import DashIconify
from utils.cytoscape import nodes_big_dipper, edges_big_dipper, nodes_orion, edges_orion, nodes_scorpion, \
    edges_scorpion, constellation
from random import sample
import json
import datetime
import os

LOTTIE_URL = 'https://lottie.host/bd952b99-002b-42d6-875e-57a7924ce27c/pEXSm4MJxX.json'
LOTTIE_OPTIONS = dict(loop=True, autoplay=True)

dash.register_page(
    __name__,
    image='assets/historical.png',
    title='Space Exploration | Historical',
    description='Dive into the key milestones of space exploration, presented in a unique cytoscape constellation '
                'format. Each point represents a significant event, complete with descriptions and images'
)

with open('utils/data/historical_data.json', 'r', encoding='utf-8') as json_file:
    historical_data = json.load(json_file)

all_years = [int(item['DATE'].split(',')[-1].strip()) for item in historical_data] + [1950]
MIN_YEARS, MAX_YEARS = min(all_years), max(all_years)
YEAR_BOUND_INF, YEAR_BOUND_SUP, YEAR_INCREMENT = 1940, 2021, 20


def right_content(*, date, country, description, image):
    return [
        dmc.Title(date, color='white', align='center'),
        dmc.Container(
            children=[
                dmc.Image(
                    src=image,
                    width='100%',
                    height='100%',
                    #radius=4,
                    withPlaceholder=True,
                    #style={'border-radius': '50%'},
                    styles={
                        'placeholder': {'background-color': '#000000'},
                        'image': {'border-radius': '50%', 'object-fit': 'cover'}
                    },
                ),
            ],
            px=0,
        ),
        dmc.Title(', '.join(country) if isinstance(country, list) else country, order=3, color='white',
                  align='center'),
        dmc.Text([description], color='white', align='center')
    ]


layout = dmc.Grid(
    [
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
                            value=[MIN_YEARS, MAX_YEARS],
                            min=MIN_YEARS,
                            max=MAX_YEARS,
                            minRange=1,
                            marks=[
                                {'value': i, 'label': i} for i in range(YEAR_BOUND_INF, YEAR_BOUND_SUP, YEAR_INCREMENT)
                            ],
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
        dcc.Store(id='historical-data', data=None),
        dcc.Store(id='range-historical-data', data=[MIN_YEARS, MAX_YEARS])
    ],
)


@callback(
    Output('cyto-constellation', 'elements'),
    Input('refresh-btn', 'n_clicks'),
    Input('range-historical-data', 'data')
)
def update_cytoscape(_, year_range):
    import pprint
    pp = pprint.PrettyPrinter()
    pp.pprint(dash.page_registry.values())
    nodes = nodes_big_dipper + nodes_orion + nodes_scorpion
    edges = edges_big_dipper + edges_orion + edges_scorpion

    scaled_data = [item for item in historical_data if
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


@callback(Output('range-historical-data', 'data'), Input('year-slider', 'value'))
def update_year_range(year_range):
    return year_range

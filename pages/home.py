import dash
from dash import dcc, Input, Output, State, clientside_callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_extensions as de
from assets.choropleth import fig

# TODO:
# Corriger responsive : text trop large, et trop d'espace globe sur mobile
# 3e page: en rapport avec les lancements/rockets/argent/coût (sous page)
# genre à droite (right content) nav burger
# à gauche contenu des mini pages, par exemple des mini card avec mini graph et quand on clique dessus
    #  -> effet modal avec + d'options

CHOROPLETH_INTERVAL = 50

url = 'https://lottie.host/bd952b99-002b-42d6-875e-57a7924ce27c/pEXSm4MJxX.json'
options = dict(loop=True, autoplay=True)

dash.register_page(__name__, path='/', title='Space Exploration | Home')

layout = dmc.Grid(
    [
        dmc.Col(
            [
                dmc.Space(className='main-space', h=20),
                de.Lottie(url=url, options=options, isClickToPauseDisabled=True),
                dmc.Stack(
                    children=[
                        dmc.Title('A little story about space..', style={'color': 'white'}, align='center'),
                        dmc.Center(
                            [
                                dmc.Text(
                                    children=[
                                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean in faucibus '
                                        'augue, rutrum placerat mi. Quisque dapibus turpis id sem laoreet, eu viverra '
                                        'mauris ultrices.'
                                    ],
                                    style={'color': 'white', 'width': '50%'},
                                    align='center',
                                    id='main-text'
                                ),
                            ]
                        ),
                        dcc.Link(
                            [
                                dmc.Button(
                                    'start',
                                    id='start-btn',
                                    variant='outline',
                                    color='white',
                                    size='lg',
                                    uppercase=True,
                                    rightIcon=DashIconify(icon='ion:rocket-outline', width=30)
                                ),
                            ],
                            href='/historical'
                        )
                    ],
                    align='center',
                    className='stack-left-container',
                    spacing=30,
                    mt=-170
                )
            ],
            md=12, lg=8
        ),
        dmc.Col(
            [
                dmc.Center(
                    [
                        dcc.Graph(
                            id='scatter-geo-fig',
                            className='graph-container',
                            figure=fig,
                            responsive=True,
                            config={
                                'displayModeBar': False,
                                'scrollZoom': False,
                                'doubleClick': False,
                            }
                        ),
                    ], className='right-container'
                ),
            ], md=12, lg=4
        ),
        dcc.Interval(id='choropleth-interval', interval=CHOROPLETH_INTERVAL),
    ],
    id='home-grid',
    className='hide',
)

clientside_callback(
    """
    function(className) {
        return "fade-in";
    }
    """,
    Output('home-grid', 'className'),
    Input('home-grid', 'className'),
)

clientside_callback(
    """
    function(_, figure) {
        var rotation_lon = figure.layout.geo.projection.rotation.lon;
        var rotation_lat = figure.layout.geo.projection.rotation.lat;

        if (rotation_lon <= -180) {
            rotation_lon = 180;
        }

        if (rotation_lon >= 180) {
            rotation_lon = -180;
        }

        if (rotation_lat >= 90) {
            rotation_lat = 90;
        } else if (rotation_lat <= -90) {
            rotation_lat = -90;
        }

        if (Math.abs(0 - rotation_lat) <= 0.01) {
            rotation_lat = 0;
        }

        const updatedFigure = Object.assign({}, figure);
        updatedFigure.layout.geo.projection.rotation.lon = rotation_lon + 0.5;
        updatedFigure.layout.geo.projection.rotation.lat = rotation_lat;

        return updatedFigure;
    }
    """,
    Output('scatter-geo-fig', 'figure'),
    Input('choropleth-interval', 'n_intervals'),
    State('scatter-geo-fig', 'figure'),
    prevent_initial_call=True
)

# 0.3 avec 10ms
# from math import isclose
#
# @callback(
#     Output('scatter-geo-fig', 'figure'),
#     Input('choropleth-interval', 'n_intervals'),
#     # Input('up', 'n_clicks'),
#     State('scatter-geo-fig', 'figure'),
#     prevent_initial_call=True
# )
# def update_rotation(_, figure):
#     rotation_lon = figure['layout']['geo']['projection']['rotation']['lon']
#     rotation_lat = figure['layout']['geo']['projection']['rotation']['lat']
#     # print(f'Rot lon : {rotation_lon} | Rot lat : {rotation_lat}')
#
#     if rotation_lon <= -180:
#         rotation_lon = 180
#     if rotation_lon >= 180:
#         rotation_lon = -180
#
#     if rotation_lat >= 90:
#         rotation_lat = 90
#     elif rotation_lat <= -90:
#         rotation_lat = -90
#
#     if isclose(0, rotation_lat, abs_tol=0.01):
#         rotation_lat = 0
#
#     return fig.update_geos(projection_rotation_lon=rotation_lon + 1, projection_rotation_lat=rotation_lat)

# 0.2

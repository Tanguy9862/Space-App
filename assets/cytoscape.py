import dash_cytoscape as cyto


def to_nodes(a, b, pos):
    return [
        {
            'data': {'id': str(i)},
            'position': {'x': pos[i-a]['x'], 'y': pos[i-a]['y']},
            'locked': False,
            'grabbable': False,
        } for i in range(a, b)]


# BIG DIPPER CONSTELLATION
pos_big_dipper = [
    {'x': 657.9974439717341, 'y': -462.4492909014162},
    {'x': 1003.3841248969776, 'y': -622.096724533191},
    {'x': 1241.165900986565, 'y': -578.4990365845125},
    {'x': 1605.9662170661804, 'y': -524.5306018693644},
    {'x': 2315.3569961765083, 'y': -736.4551918594866},
    {'x': 2344.536591838474, 'y': -369.722231142429},
    {'x': 1781.5141773273285, 'y': -244.38632679206094}
]

nodes_big_dipper = to_nodes(*(0, 7), pos=pos_big_dipper)

edges_big_dipper = [
    {
        'data': {
            'source': str(i),
            'target': str(i+1)
        },
        'selectable': False
    } if i < 6 else {'data': {'source': str(i), 'target': str(3)}, 'selectable': False}
    for i in range(7)
]

# ORION CONSTELLATION
pos_orion = [
    {'x': -1051.801882309906, 'y': 1116.2561824716317},
    {'x': -276.91892787126574, 'y': 1016.8941968633548},
    {'x': -476.06704195867246, 'y': 463.6822924231584},
    {'x': -589.3344778706902, 'y': 521.0098746200957},
    {'x': -708.2303453858251, 'y': 558.0627958382067},
    {'x': -797.0474765455318, 'y': -36.848259195809796},
    {'x': -856.7539244698986, 'y': -186.26115504454344},
    {'x': -830.8831255120091, 'y': -455.9908847136578},
    {'x': -931.4413824878276, 'y': -422.81112017523304},
    {'x': -640.2451879814284, 'y': -665.1243775940777},
    {'x': -772.1164198972962, 'y': -661.9483360519431},
    {'x': -389.25675726159085, 'y': 41.76909584769615},
    {'x': -544.6563190757502, 'y': -155.7191094747217},
    {'x': 239.85895419154764, 'y': -177.12378974219078},
    {'x': 154.99096617220331, 'y': -295.3750871092268},
    {'x': 32.267339075516055, 'y': -407.94333594280903},
    {'x': 236.89706373577334, 'y': -48.36149173345387},
    {'x': 215.5649087845008, 'y': 148.37752438203844},
    {'x': 112.02174889388361, 'y': 238.065677115606}
]

nodes_orion = to_nodes(*(7, 26), pos=pos_orion)

edges_orion = [
    {'data': {'source': '7', 'target': '8'}},
    {'data': {'source': '7', 'target': '11'}},
    {'data': {'source': '8', 'target': '9'}},
    {'data': {'source': '9', 'target': '10'}},
    {'data': {'source': '10', 'target': '11'}},
    {'data': {'source': '11', 'target': '12'}},
    {'data': {'source': '12', 'target': '13'}},
    {'data': {'source': '13', 'target': '14'}},
    {'data': {'source': '13', 'target': '15'}},
    {'data': {'source': '14', 'target': '16'}},
    {'data': {'source': '14', 'target': '15'}},
    {'data': {'source': '15', 'target': '17'}},
    {'data': {'source': '9', 'target': '18'}},
    {'data': {'source': '18', 'target': '19'}},
    {'data': {'source': '19', 'target': '12'}},
    {'data': {'source': '18', 'target': '20'}},
    {'data': {'source': '20', 'target': '21'}},
    {'data': {'source': '21', 'target': '22'}},
    {'data': {'source': '20', 'target': '23'}},
    {'data': {'source': '23', 'target': '24'}},
    {'data': {'source': '24', 'target': '25'}}
]
edges_orion = [dict(item, **{'selectable': False}) for item in edges_orion]

pos_scorpion = [
    {'x': 1893.4276029197683, 'y': 766.8868229227538},
    {'x': 1997.9678921186785, 'y': 898.378357811615},
    {'x': 2065.225443141404, 'y': 993.4235850861587},
    {'x': 1903.5940418269715, 'y': 1129.893362889075},
    {'x': 1595.3741900210132, 'y': 1092.572553172164},
    {'x': 1386.0129062702101, 'y': 995.8942099368963},
    {'x': 1357.2217985040752, 'y': 696.0727209917395},
    {'x': 1332.6814442563743, 'y': 456.53993359302325},
    {'x': 1162.203519437309, 'y': 141.2413872953832},
    {'x': 1061.2172125150087, 'y': 8.277252310770201},
    {'x': 733.8200618663466, 'y': 109.67123000355878},
    {'x': 725.5782421780481, 'y': -39.0981527714444},
    {'x': 762.0506918373462, 'y': -215.7944927576788}
]

nodes_scorpion = to_nodes(*(26, 39), pos=pos_scorpion)

edges_scorpion = [
    {
        'data': {
            'source': str(i),
            'target': str(i+1)
        },
        'selectable': False
    } if i < 36 else {'data': {'source': str(35), 'target': str(i)}, 'selectable': False}
    for i in range(26, 39)
]

constellation = cyto.Cytoscape(
    id='cyto-constellation',
    className='constellation',
    layout={'name': 'preset'},
    style={'width': '95%', 'height': '75vh'},
    stylesheet=[
        {
            'selector': 'node',
            'style': {
                'background-color': 'white',
                'font-size': '35px',
                'text-margin-y': '-15px',
                'label': 'data(YEAR)',
                'content': 'data(YEAR)',
                'color': '#eaeaea',
            }
        },
        {
            'selector': 'node:selected',
            'style': {
                'background-color': '#D291DF', # #00f9ff
                'color': '#D291DF'
            }
        }
    ],
    zoom=0.4,
    minZoom=0.3,
    maxZoom=0.5,
    responsive=True,
)

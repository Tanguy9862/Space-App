import dash
import json
import pandas as pd
from dash import html, dcc, Output, Input, callback
from assets.footer import footer
from pages.nav import navbar
from utils.cloud_storage import read_from_gcs
from utils.past_launches_processing import clean_past_launches_data
from io import StringIO

app = dash.Dash(
    __name__,
    title='Space Exploration',
    use_pages=True,
    update_title=False,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    meta_tags=[
        {"name": "description", "content": "A Dash app focused on space exploration data."},
        {"name": "keywords", "content": "Space, Launch, Data, Visualization, Dash,"
                                        "NASA, SpaceX, Rocket, Satellite, Mars, Moon, Astronaut, Space Station, "
                                        "Orbital, Galaxy, Universe, Telemetry, Spacecraft, Interstellar, Cosmonaut, "
                                        "Astrobiology, Exoplanet, Space Shuttle, Space Mission, Space Probe, Hubble, "
                                        "Space Tourism, Space Colony, Zero Gravity, Deep Space"}
    ],
)

server = app.server

app.layout = html.Div(
    [
        navbar(),
        dash.page_container,
        footer,
        dcc.Store('past-launches-data', data=None),
        dcc.Store('next-launch-data', data=None),
        dcc.Store('last-update', data=None),
    ],
)


@callback(
    Output('past-launches-data', 'data'),
    Input('past-launches-data', 'id'),
)
def load_past_launches_data(_):
    df = pd.read_csv(StringIO(read_from_gcs('past_launches_data.csv').download_as_text()))
    df = clean_past_launches_data(df)
    return df.to_dict('records')


@callback(
    Output('next-launch-data', 'data'),
    Input('next-launch-data', 'id'),
)
def load_next_launch_data(_):
    return json.loads(read_from_gcs('next_launch_data.json').download_as_text())


if __name__ == "__main__":
    app.run_server(debug=True)

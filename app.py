import dash
import logging
import pandas as pd
from dash import html, dcc, Output, Input, callback, ALL

from config import CONFIG
from assets.footer import footer
from pages.nav import navbar
from utils.loading_data import load_data

pd.set_option('display.max_colwidth', None)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

logging.info(f"Environment chosen: {CONFIG.ENV}")

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
        dcc.Store('past-launches-data'),
        dcc.Store(id='past-launches-last-update'),
        dash.page_container,
        footer,
    ]
)


@callback(
    Output('historical-data', 'data'),
    Output('historical-facts-last-update', 'data'),
    Input('historical-data', 'id'),
)
def load_historical_facts_data(_):
    return load_data('HISTORICAL_FACTS_FILENAME', 'json')


@callback(
    Output('past-launches-data', 'data'),
    Output('past-launches-last-update', 'data'),
    Input('past-launches-data', 'id'),
)
def load_past_launches_data(_):
    df, last_update = load_data('PAST_LAUNCHES_FILENAME', 'csv')
    return df.to_dict('records'), last_update


@callback(
    Output('next-launch-data', 'data'),
    Output('next-launch-last-update', 'data'),
    Input('next-launch-data', 'id'),
)
def load_next_launch_data(_):
    return load_data('NEXT_LAUNCH_FILENAME', 'json')


if __name__ == "__main__":
    app.run_server(debug=True)

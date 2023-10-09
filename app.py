import dash
from dash import html
from assets.footer import footer
from pages.nav import navbar

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
        footer
    ],
)

if __name__ == "__main__":
    app.run_server(debug=False)

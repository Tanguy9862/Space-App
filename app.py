import dash
from dash import html
import dash_mantine_components as dmc

# LAYOUT
from assets.footer import footer
from pages.nav import navbar

app = dash.Dash(
    __name__,
    use_pages=True,
    update_title=False,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)

app.layout = html.Div(
    [
        navbar(),
        dash.page_container,
        footer
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)

import dash
from dash import html
import dash_mantine_components as dmc

# LAYOUT
from assets.footer import footer

from pages.nav import navbar

# TODO :
# En faire un vrai projet data science :
    # scrapper les donnnées sur le site original
    # data pre processing
    # utiliser wikipedia api
    # faire un readme sur github, expliquer la démarche
# Seconde page, animation ? utiliser eventlistener de dash extension ? ou bien callback basique comme j'avais fait?
# Historique : constellation, 1 pt = 1 année
    # description à droite à la place de la terre : titre, image, pays, desc.
    # slider année
    # dropdown constelellation
# Tout le pre processing de choropleth : générer un fichier csv déjà préparé et propre

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

import dash
import dash_mantine_components as dmc
import dash_extensions as de

url = 'https://lottie.host/ddf21357-3e6a-4c62-a706-c072c9a4f038/1Fz4LEXRnF.json'
options = dict(loop=True, autoplay=True)

dash.register_page(
    __name__,
    path="/404",
    title='Space Exploration | Not Found'
)


layout = dmc.Container(
    [
        de.Lottie(
            url=url,
            options=options,
            isClickToPauseDisabled=True,
            width='550px',
        )
    ],
    style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'height': '100vh',
    },
)

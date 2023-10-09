import dash
import dash_mantine_components as dmc
import dash_extensions as de

#url = 'https://lottie.host/bf9ef8a4-4131-4ee4-ba6b-5efd0af9b9b5/bVXji3xcFZ.json'
#url = 'https://lottie.host/17bc172c-68fe-4ba5-b236-cf16fed45479/Y8eQOh5BpD.json'
#url = 'https://lottie.host/5f37e8f1-b124-41ae-96a4-f57a620ab08e/c546VS6RnM.json'
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

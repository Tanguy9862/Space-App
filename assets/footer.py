import dash_mantine_components as dmc
from dash_iconify import DashIconify

GITHUB = 'https://github.com/tanguy9862'
LINKEDIN = 'https://fr.linkedin.com/in/tanguy-surowiec-69aa79222'
CONTACT_ICON_WIDTH = 25

footer = dmc.Grid(
    [
        dmc.Col(
            [
                dmc.Footer(
                    height=30,
                    fixed=True,
                    className='footer-container',
                    style={
                        'backgroundColor': 'rgba(0,0,0,0)',
                    },
                    mb=5,
                    withBorder=False,
                    children=[
                        dmc.Group(
                            children=[
                                dmc.Anchor(
                                    children=[DashIconify(
                                        icon='mdi:github', width=CONTACT_ICON_WIDTH)
                                    ],
                                    href=GITHUB
                                ),
                                dmc.Anchor(
                                    children=[
                                        DashIconify(
                                            icon='ri:linkedin-fill', width=CONTACT_ICON_WIDTH)
                                    ],
                                    href=LINKEDIN
                                )
                            ], position='center'
                        )
                    ]
                )
            ], span=12
        )
    ]
)

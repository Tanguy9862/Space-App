from dash import dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def create_notification(page, date: str, data_type: str, freq: str):
    return dmc.Notification(
            id=f'{page}-notification',
            title=f'{data_type} Last Updated (checked {freq})',
            action='show',
            message=dcc.Markdown(
                f"""
                {date}
                
                Updates are applied only when new information is available.               
                """
            ),
            autoClose=False,
            icon=DashIconify(icon='material-symbols:system-update-alt'),
            style={'background-color': 'rgba(0, 0, 0, 0)', 'border': 'none', 'color': 'white'},
            styles={
                'title': {'color': 'white'},
                'description': {'color': '#E6E6E6'}
            }
    )

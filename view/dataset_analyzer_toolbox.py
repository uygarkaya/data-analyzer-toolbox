from dash import Dash, html
from .components.header import Header
from .components.footer import Footer

import dash_bootstrap_components as dbc

class DatasetAnalyzerToolbox:
    def __init__(self):
        self.app = Dash(
            __name__, 
            external_stylesheets=[
                dbc.themes.BOOTSTRAP,
                "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
            ],
            suppress_callback_exceptions=True, 
            title='Dataset Analyzer Toolbox'
        )

        self.app.layout = self.serve_app_layout()
    
    def serve_app_layout(self):
        return html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'column',
                'height': '100vh',
            },
            children=[
                Header().header(),
                html.Div(
                    children=[
                        html.Div(id='page-content', style={'flex': 1, 'overflowY': 'auto'}),
                    ],
                    style={
                        'flex': 1,
                        'overflowY': 'auto',
                        'marginBottom': '3em',
                        'display': 'flex',
                    },
                ),
                Footer().footer(),
            ]
        )

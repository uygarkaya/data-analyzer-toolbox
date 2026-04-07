from dash import Dash, html, dcc
from .components.header import Header
from .components.footer import Footer
from .components.center import Center
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
            prevent_initial_callbacks="initial_duplicate",
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
                    id="upload-alert-container",
                    style={
                        "position": "fixed",
                        # "top": "20px",
                        "right": "20px",
                        "zIndex": 9999,
                    }
                ),
                html.Div(
                    children=[
                        Center().center(),
                    ],
                    style={
                        'flex': 1,
                        'minHeight': 0,
                        'marginBottom': '3em',
                        'display': 'flex',
                        'height': '100%',
                        'width': '100%',
                    },
                ),
                Footer().footer(),
            ]
        )

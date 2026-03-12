from dash import Dash
import dash_bootstrap_components as dbc

class DatasetAnalyzerToolbox:
    def __init__(self):
        self.app = Dash(
            __name__, 
            external_stylesheets=[
                dbc.themes.CYBORG,
                "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
            ],
            suppress_callback_exceptions=True, 
            title='Dataset Analyzer Toolbox'
        )
import dash_bootstrap_components as dbc
from dash import html, get_asset_url

class Header:
    def __init__(self) -> None:
        pass

    def header(self) -> html.Div:
        return dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src=get_asset_url('logo.svg'),
                            style={"height": "100%", "maxHeight": "60px"}
                        ),
                        width=5,
                        style={
                            "padding": "0.4em",
                            "height": "60px",
                            "width": "60px",
                            "backgroundColor": "#125A9E"
                        }
                    ),
                    dbc.Col(
                        html.Div(
                            "Dataset Analyzer Toolbox",
                            style={
                                "fontSize": "1.3rem",
                                "color": "#ffffff",
                                "padding": "0.3em",
                                "height": "60px",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "start",
                                "fontFamily": "sans-serif",
                                "padding-left": "10px",
                            }
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            id="alert-container", 
                            style={
                                "height": "60px", 
                                "width": "100%", 
                                "display": "flex", 
                                "alignItems": "center", 
                                "justifyContent": "end",
                                "padding-top": "1em",
                                "fontFamily": "sans-serif",
                            }
                        )
                    ),
                ],
                className="d-flex",
            ),
            fluid=True,
            style={
                "top": "0",
                "zIndex": "100",
                "position": "sticky",
                "marginBottom": "1em",
                "backgroundImage": "linear-gradient(to right, #0E9D59, #00898D)"
            }
        )

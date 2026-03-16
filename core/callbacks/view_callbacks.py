from dash import html, dcc 
from dash import callback, Output, Input 
import dash_bootstrap_components as dbc 

class ViewCallbacks:
    def __init__(self) -> None:
        pass

    def register_callbacks(self, app):
        @callback(
            Output("fetch-data-tab-content", "children"),
            Input("fetch-data-tabs", "value")
        )
        def fetch_data_tabs(value):
            if value == "fetch-data-upload":
                return dcc.Upload(
                    id="upload-dataset",
                    children=html.Div(
                        [
                            html.Div("Drag & Drop File Here!"),
                            html.Small("or Click to Select File"),
                            html.Div("Supported Formats: CSV")
                        ],
                        style={"textAlign": "center"}
                    ),
                    style={
                        "width": "100%",
                        "height": "120px",
                        "borderWidth": "2px",
                        "borderStyle": "dashed",
                        "borderRadius": "10px",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "cursor": "pointer",
                        "transition": "all 0.2s",
                        "backgroundColor": "#F8F9FA"
                    },
                    multiple=False
                )
            elif value == "fetch-data-sample":
                return html.Div(
                    [
                        html.H6("Select a sample dataset to load:"),
                        dbc.ListGroup(
                            [
                                dbc.ListGroupItem("01 - Dataset: Iris", id="sample-iris", action=True, style={"transition": "all 0.2s"}),
                                dbc.ListGroupItem("02 - Dataset: Titanic", id="sample-titanic", action=True, style={"transition": "all 0.2s"}),
                                dbc.ListGroupItem("03 - Dataset: Wine Quality", id="sample-wine", action=True, style={"transition": "all 0.2s"}),
                            ]
                        )
                    ]
                )
            else:
                return dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                id="api-url",
                                placeholder="https://api.example.com/dataset",
                                type="text"
                            ),
                            width=9
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Fetch Data",
                                id="fetch-api-btn",
                                color="primary",
                                className="w-100"
                            ),
                            width=3
                        )
                    ]
                )
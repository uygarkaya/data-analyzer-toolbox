from configuration.configuration import Configuration
from core.view.dataset_analyzer_toolbox import DatasetAnalyzerToolbox
from dash import Output, Input 
from dash import html, dcc 
import dash_bootstrap_components as dbc
import pandas as pd

class ViewCallbacks:
    def __init__(self, view: DatasetAnalyzerToolbox) -> None:
        self.view = view

    def register_callbacks(self):
        @self.view.app.callback(
            Output("fetch-data-tab-content", "children"),
            Input("fetch-data-tabs", "value")
        )
        def fetch_data_tabs(value):
            if value == "fetch-data-upload":
                return dcc.Upload(
                    id="upload-dataset",
                    children=html.Div(
                        [
                            html.Img(
                                src="https://cdn-icons-png.flaticon.com/512/3097/3097412.png",
                                style={
                                    "width": "50px",
                                    "marginBottom": "10px",
                                    "opacity": "0.7"
                                }
                            ),
                            html.Div(
                                "Drag & Drop File Here",
                                style={
                                    "fontSize": "16px",
                                    "fontWeight": "600",
                                    "color": "#333"
                                }
                            ),
                            html.Small(
                                "or Click to Browse",
                                style={"color": "#777"}
                            ),
                            html.Div(
                                "Supported Format: CSV",
                                style={
                                    "marginTop": "5px",
                                    "fontSize": "12px",
                                    "color": "#999"
                                }
                            ),
                        ],
                        style={
                            "textAlign": "center",
                            "display": "flex",
                            "flexDirection": "column",
                            "alignItems": "center",
                            "justifyContent": "center",
                        }
                    ),
                    style={
                        "width": "100%",
                        "height": "150px",
                        "borderWidth": "2px",
                        "borderStyle": "dashed",
                        "borderRadius": "16px",
                        "borderColor": "#6C63FF",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "cursor": "pointer",
                        "backgroundColor": "#F9FAFF",
                        "transition": "all 0.3s ease",
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.05)",
                    },
                    multiple=False
                )
            elif value == "fetch-data-sample":
                return html.Div(
                    [
                        dbc.ListGroup(
                            [
                                dbc.ListGroupItem(
                                    dataset["name"],
                                    id={"type": "sample-dataset-btn", "index": dataset["id"]},
                                    action=True,
                                    color="light"
                                )
                                for dataset in Configuration().sample_datasets
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
            
        @self.view.app.callback(
            Output("dataset-preview", "children"),
            Input("stored-dataset", "data")
        )
        def update_preview(data):
            if data is None:
                return "No Dataset Loaded Yet!"

            df = pd.DataFrame(data)

            return html.Div(
            [
                html.Div(
                    dbc.Table.from_dataframe(
                        df.sample(10, random_state=42).reset_index(drop=True),
                        striped=True,
                        bordered=True,
                        hover=True,
                        size="sm",
                        responsive=True,
                    ),
                    style={
                        "maxHeight": "300px",
                        "overflowY": "auto",
                        "border": "1px solid #dee2e6",
                        "borderRadius": "6px",
                        "boxShadow": "inset 0 1px 3px rgba(0,0,0,0.1)",
                        "backgroundColor": "#fff",
                    }
                )
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "gap": "8px",
                "backgroundColor": "#f8f9fa",
                "borderRadius": "8px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.05)"
            }
        )
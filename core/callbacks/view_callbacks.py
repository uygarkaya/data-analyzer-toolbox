from configuration.configuration import Configuration
from core.view.data_analyzer_toolbox import DataAnalyzerToolbox
from utils.helpers import HelperFunc
from dash import Output, Input 
from dash import html, dcc 
import dash_bootstrap_components as dbc
import pandas as pd

class ViewCallbacks:
    def __init__(self, view: DataAnalyzerToolbox) -> None:
        self.view = view

    def register_callbacks(self):
        @self.view.app.callback(
            Output("fetch-data-tab-content", "children"),
            Input("fetch-data-tabs", "value")
        )
        def fetch_data_tabs(value):
            if value == "fetch-data-upload":
                return html.Div(
                    [
                        dcc.Upload(
                            id="upload-dataset",
                            children=html.Div(
                                [
                                    html.Div(
                                        html.Img(
                                            src="https://cdn-icons-png.flaticon.com/512/3097/3097412.png",
                                            style={
                                                "width": "60px",
                                                "opacity": "0.9",
                                            }
                                        ),
                                        style={
                                            "width": "104px",
                                            "height": "104px",
                                            "borderRadius": "50%",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "background": "#FFFFFF",
                                            "boxShadow": "0 4px 14px rgba(108,99,255,0.10), inset 0 0 0 1px rgba(108,99,255,0.10)",
                                            "marginBottom": "16px",
                                        }
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                html.Span(
                                                    "Drag & Drop Your File",
                                                    style={
                                                        "fontSize": "15px",
                                                        "fontWeight": "600",
                                                        "color": "#2B2D42",
                                                    }
                                                )
                                            ),
                                            html.Div(
                                                html.Span(
                                                    "OR",
                                                    style={
                                                        "fontSize": "15px",
                                                        "color": "#8A8FA3",
                                                    }
                                                )
                                            ),
                                            html.Div(
                                                html.Span(
                                                    "BROWSE",
                                                    style={
                                                        "fontSize": "15px",
                                                        "fontWeight": "600",
                                                        "color": "#6C63FF",
                                                        "borderBottom": "1px dashed #6C63FF",
                                                    }
                                                )
                                            ),
                                        ],
                                        style={"marginBottom": "10px"}
                                    ),
                                    html.Div(
                                        [
                                            html.Span(
                                                "SUPPORTED FILE TYPE: CSV",
                                                style={
                                                    "fontSize": "10px",
                                                    "fontWeight": "700",
                                                    "letterSpacing": "0.08em",
                                                    "color": "#6C63FF",
                                                    "backgroundColor": "rgba(108,99,255,0.10)",
                                                    "padding": "3px 8px",
                                                    "borderRadius": "10px",
                                                }
                                            )
                                        ],
                                        style={
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
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
                                "height": "240px",
                                "borderWidth": "1.5px",
                                "borderStyle": "dashed",
                                "borderRadius": "16px",
                                "borderColor": "rgba(108,99,255,0.45)",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "cursor": "pointer",
                                "background": "#FFFFFF",
                                "transition": "all 0.25s ease",
                                "boxShadow": "0 6px 20px rgba(108,99,255,0.06)",
                            },
                            multiple=False
                        )
                    ]
                )
            elif value == "fetch-data-sample":
                return html.Div(
                    dbc.Row(
                        [HelperFunc.sample_dataset_card(d) for d in Configuration().sample_datasets],
                        className="g-3",
                    ),
                    style={"padding": "4px"},
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
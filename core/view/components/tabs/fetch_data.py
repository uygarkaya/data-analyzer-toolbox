from dash import html, dcc 
import dash_bootstrap_components as dbc 

class FetchData:
    def __init__(self) -> None:
        pass

    def content(self) -> html.Div:
        return html.Div(
            [
                dcc.Store(id="stored-dataset", storage_type="memory"),
                html.Div(
                    [
                        html.H4(
                            "Fetch & Load Dataset",
                            style={"fontWeight": "700"}
                        ),
                        html.H6(
                            "Upload Your Own Dataset, Load a Sample Dataset, or Fetch From an API Endpoint!",
                            style={"color": "#6c757d"}
                        ),
                    ],
                    style={"marginBottom": "15px"}
                ),

                dbc.Card(
                    [
                        dbc.CardHeader(
                            dcc.Tabs(
                                id="fetch-data-tabs",
                                value="fetch-data-sample",
                                children=[
                                    dcc.Tab(
                                        label=label,
                                        value=value,
                                        style={
                                            "padding": "6px 14px",
                                            "fontSize": "0.80rem",
                                            "fontWeight": "700",
                                            "letterSpacing": "0.05em",
                                            "textTransform": "uppercase",
                                            "border": "none",
                                            "backgroundColor": "transparent"
                                        },
                                        selected_style={
                                            "padding": "6px 14px",
                                            "fontSize": "0.80rem",
                                            "fontWeight": "700",
                                            "letterSpacing": "0.05em",
                                            "textTransform": "uppercase",
                                            "border": "none",
                                            "backgroundColor": "transparent",
                                            "borderBottom": "2px solid #0d6efd",
                                            "color": "#0D6EFD"
                                        },
                                    )
                                    for label, value in [
                                        ("SAMPLE DATASETS", "fetch-data-sample"),
                                        ("UPLOAD FILE", "fetch-data-upload"),
                                        ("FETCH FROM API", "fetch-data-api"),
                                    ]
                                ],
                                parent_style={
                                    "height": "38px",
                                },
                            )
                        ),

                        dbc.CardBody(
                            html.Div(id="fetch-data-tab-content")
                        )
                    ],
                    style={
                        "borderRadius": "16px",
                        "overflow": "hidden",
                        "boxShadow": "0 4px 15px rgba(0,0,0,0.1)"
                    },
                    className="shadow-sm"
                ),
                html.Hr(),
                dbc.Card(
                    [
                        dbc.CardHeader(
                            html.Div(
                                [
                                    html.Span("🔍", style={"marginRight": "6px"}),
                                    html.Strong("Dataset Preview")
                                ]
                            )
                        ),

                        dbc.CardBody(
                            html.Div(
                                "No Dataset Loaded Yet!",
                                id="dataset-preview",
                                style={
                                    "color": "#6C757D",
                                    "textAlign": "center",
                                    "padding": "30px"
                                }
                            )
                        )
                    ],
                    style={
                        "borderRadius": "16px",
                        "overflowY": "auto",

                    },
                    className="shadow-sm"
                )
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "gap": "10px",
                "width": "100%",
                "height": "100%",
            }
        )
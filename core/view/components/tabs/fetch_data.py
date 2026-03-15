import dash_bootstrap_components as dbc
from dash import html, dcc


class FetchData:
    def __init__(self) -> None:
        pass

    def content(self) -> html.Div:
        return html.Div(
            [
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

                dbc.Tabs(
                    [
                        dbc.Tab(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dcc.Upload(
                                            id="upload-dataset",
                                            children=html.Div(
                                                [
                                                    html.Div("Drag & Drop CSV File Here!"),
                                                    html.Small("or Click to Select File")
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
                                                "cursor": "pointer"
                                            },
                                            multiple=False
                                        )
                                    ]
                                )
                            ), 
                            label="Upload File"
                        ),
                        dbc.Tab(
                            dbc.Card(
                                dbc.CardBody(
                                [
                                    html.H6("Select a sample dataset to load:"),
                                    dbc.ListGroup(
                                        [
                                            dbc.ListGroupItem("01 - Dataset: Iris", id="sample-iris", action=True),
                                            dbc.ListGroupItem("02 - Dataset: Titanic", id="sample-titanic", action=True),
                                            dbc.ListGroupItem("03 - Dataset: Wine Quality", id="sample-wine", action=True),
                                        ]
                                    )
                                ]
                            )),
                            label="Sample Datasets"
                        ),
                        dbc.Tab(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Input(
                                                        id="api-url",
                                                        placeholder="Enter API endpoint returning JSON / CSV",
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
                                        ),

                                        html.Small(
                                            "Example: https://api.example.com/dataset",
                                            style={"color": "#6c757d"}
                                        )
                                    ]
                                )
                            ), 
                            label="Fetch from API"
                        ),
                    ]
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
                                    "color": "#6c757d",
                                    "textAlign": "center",
                                    "padding": "30px"
                                }
                            )
                        )
                    ],
                    style={
                        "borderRadius": "16px"
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
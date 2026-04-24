from dash import html, dcc
from pathlib import Path
from utils.constants import TYPE_STYLES

import dash_bootstrap_components as dbc
import json

class HelperFunc:
    def __init__(self) -> None:
        pass

    def no_data_alert(self, msg_id, icon_class="bi bi-database-x") -> html.Div:
        return html.Div(
            id=msg_id,
            children=dbc.Alert(
                [
                    html.I(className=f"{icon_class} me-2"),
                    "No Dataset Loaded Yet. Upload or Select a Sample Dataset to Begin"
                ],
                color="danger",
                style={
                    "borderRadius": "8px",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "height": "80px",
                    "width": "100%",
                }
            ),
        )

    def build_card(
        self,
        variant: str,
        title: str = "",
        component_id: str = "",
        color: str = "#0D6EFD",
        body: list = None,
        height: str = "320px"
    ):
        body = body or []
        if variant == "stat":
            return dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div([
                            html.Span(
                                title,
                                style={
                                    "fontSize": "12px",
                                    "color": "#6C757D",
                                    "fontWeight": "600",
                                    "textTransform": "uppercase",
                                    "letterSpacing": "0.5px"
                                }
                            ),
                        ], style={
                            "display": "flex",
                            "alignItems": "center",
                            "marginBottom": "6px"
                        }),
                        html.H4(
                            id=component_id,
                            children="—",
                            style={
                                "fontWeight": "700",
                                "color": color,
                                "marginBottom": "0"
                            }
                        )
                    ]),
                    style={
                        "borderLeft": f"4px solid {color}",
                        "borderRadius": "8px",
                        "boxShadow": "0 1px 6px rgba(0,0,0,0.07)"
                    }
                ),
                xs=12,
                sm=6,
                md=3,
                style={"marginBottom": "16px"}
            )

        elif variant == "chart":
            return dbc.Card(
                dbc.CardBody([
                    html.H6(
                        title,
                        style={
                            "fontWeight": "600",
                            "marginBottom": "12px",
                            "color": "#343A40"
                        }
                    ),
                    dcc.Loading(
                        dcc.Graph(
                            id=component_id,
                            config={"displayModeBar": False},
                            style={"height": height}
                        ),
                        type="circle",
                        color=color
                    )
                ]),
                style={
                    "borderRadius": "10px",
                    "boxShadow": "0 1px 6px rgba(0,0,0,0.07)",
                    "marginBottom": "20px"
                }
            )

        elif variant == "section":
            return dbc.Card(
                [
                    dbc.CardHeader(
                        html.Div(
                            [
                                html.Span(
                                    title,
                                    style={
                                        "fontWeight": "700",
                                        "fontSize": "14px",
                                        "display": "block"
                                    }
                                )
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center"
                            }
                        )
                    ),
                    dbc.CardBody(body)
                ],
                style={
                    "borderRadius": "10px",
                    "boxShadow": "0 1px 6px rgba(0,0,0,0.07)",
                    "height": "100%"
                }
            )

        else:
            raise ValueError(f"Unsupported Card Variant: {variant}")

    def load_json(self, path: str) -> list:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"Dataset Config Not Found: {path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("Dataset JSON must be a List!")

        return data
    
    def generate_alert(self, message, color="success", duration=4000) -> dbc.Alert:
        return dbc.Alert(
            id="popup-notification",
            children=message,
            color=color,
            dismissable=True,
            duration=duration,
            style={
                "position": "fixed",
                "right": "20px",
                "zIndex": 9999,
                "minWidth": "250px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.15)",
                "borderRadius": "5px",
            }
        )
    
    def sample_dataset_card(dataset):
        meta = TYPE_STYLES.get(
            dataset.get("type", "").lower(),
            {"color": "secondary"}
        )

        return dbc.Col(
            html.Div(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        dataset["name"].split(" - ")[0] if " - " in dataset["name"] else "",
                                        style={
                                            "fontSize": "1.4rem",
                                            "fontWeight": "700",
                                            "color": "#212529",
                                            "marginRight": "10px",
                                            "letterSpacing": "0.05em",
                                        }
                                    ),
                                    dbc.Badge(
                                        dataset.get("type", "dataset").upper(),
                                        color=meta["color"],
                                        className="ms-auto",
                                        style={
                                            "fontSize": "0.65rem",
                                            "letterSpacing": "0.08em",
                                            "padding": "5px 10px",
                                        }
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "marginBottom": "10px",
                                }
                            ),
                            html.Div(
                                dataset["name"].split(" - ")[1] if " - " in dataset["name"] else dataset["name"],
                                style={
                                    "fontWeight": "700",
                                    "fontSize": "0.95rem",
                                    "color": "#212529",
                                    "marginBottom": "6px",
                                    "lineHeight": "1.3",
                                }
                            ),
                            html.Div(
                                dataset.get("description", ""),
                                style={
                                    "fontSize": "0.80rem",
                                    "color": "#6C757D",
                                    "marginBottom": "12px",
                                    "minHeight": "36px",
                                }
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "TARGET",
                                        style={
                                            "fontSize": "0.65rem",
                                            "fontWeight": "700",
                                            "color": "#ADB5BD",
                                            "letterSpacing": "0.08em",
                                            "marginRight": "6px",
                                        }
                                    ),
                                    html.Code(
                                        (dataset.get("target_col") or "—").upper(),
                                        style={
                                            "fontSize": "0.75rem",
                                            "backgroundColor": "#F1F3F5",
                                            "padding": "2px 8px",
                                            "borderRadius": "4px",
                                            "color": "#0D6EFD",
                                        }
                                    ),
                                    dbc.Badge(
                                        dataset.get("format", "csv").upper(),
                                        color="light",
                                        text_color="dark",
                                        className="ms-auto",
                                        style={
                                            "fontSize": "0.65rem",
                                            "border": "1px solid #dee2e6",
                                        }
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                    "borderTop": "1px solid #f1f3f5",
                                    "paddingTop": "10px",
                                }
                            ),
                        ]
                    ),
                    style={
                        "borderRadius": "12px",
                        "border": "1px solid #e9ecef",
                        "height": "100%",
                        "transition": "all 0.2s ease",
                        "cursor": "pointer",
                    },
                    className="sample-dataset-card h-100 shadow-sm",
                ),
                id={"type": "sample-dataset-btn", "index": dataset["id"]},
                n_clicks=0,
                style={"cursor": "pointer", "height": "100%"},
            ),
            xs=12, sm=6, lg=6, xl=4,
            className="mb-3",
        )
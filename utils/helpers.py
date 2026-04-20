from dash import html, dcc
from pathlib import Path
import json
import dash_bootstrap_components as dbc

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
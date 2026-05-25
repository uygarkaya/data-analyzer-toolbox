from dash import html, dcc
from utils.helpers import HelperFunc
from utils.constants import CARD_STYLE, SECTION_DIVIDER_STYLE
import dash_bootstrap_components as dbc

class WhatIf:
    def __init__(self) -> None:
        self.helper_func = HelperFunc()

    def _config_card(self) -> dbc.Card:
        label = self.helper_func.field_label
        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Span(
                        "Configure Counterfactual Scenario",
                        style={"fontWeight": "700", "fontSize": "14px"},
                    )
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        label("Feature to Simulate"),
                                        dcc.Dropdown(
                                            id="wi-feature-select",
                                            placeholder="Choose a feature…",
                                            clearable=False,
                                            style={"fontSize": "13px"},
                                        ),
                                    ],
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        label("Simulation Type"),
                                        dcc.Dropdown(
                                            id="wi-pert-type",
                                            options=[
                                                {"label": "Set Feature Value (counterfactual)", "value": "set_value"},
                                                {"label": "Gaussian Noise (× std)", "value": "noise"},
                                            ],
                                            value="set_value",
                                            clearable=False,
                                            style={"fontSize": "13px"},
                                        ),
                                    ],
                                    md=4,
                                ),
                                dbc.Col(
                                    [
                                        label("Rows to Simulate (%)"),
                                        dcc.Slider(
                                            id="wi-sample-frac",
                                            min=10, max=100, step=10, value=100,
                                            marks={i: f"{i}" for i in range(10, 101, 10)},
                                            tooltip={"placement": "bottom", "always_visible": False},
                                        ),
                                    ],
                                    md=4,
                                ),
                            ],
                            className="g-3",
                        ),
                        html.Hr(style={**SECTION_DIVIDER_STYLE, "margin": "16px 0"}),
                        html.Div(
                            id="wi-pert-param-wrap",
                            children=[
                                html.Label(
                                    id="wi-pert-param-label",
                                    style={"fontWeight": "600", "fontSize": "12px",
                                           "display": "block", "marginBottom": "6px"},
                                ),
                                html.Div(id="wi-intervention-control"),
                            ],
                        ),
                        html.Hr(style={**SECTION_DIVIDER_STYLE, "margin": "16px 0"}),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        [html.I(className="bi bi-play-fill me-2"), "Run Simulation"],
                                        id="wi-run-btn",
                                        color="primary",
                                        className="w-100",
                                    ),
                                    md=6,
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        [html.I(className="bi bi-arrow-counterclockwise me-2"), "Reset"],
                                        id="wi-reset-btn",
                                        color="secondary",
                                        outline=True,
                                        className="w-100",
                                    ),
                                    md=6,
                                ),
                            ],
                            className="g-2",
                        ),
                    ]
                ),
            ],
            style={**CARD_STYLE, "marginBottom": "20px"},
        )

    def _metrics_card(self) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Span(
                        "Performance: Baseline vs Counterfactual",
                        style={"fontWeight": "700", "fontSize": "14px"},
                    )
                ),
                dbc.CardBody(
                    dcc.Loading(html.Div(id="wi-metrics"), type="circle"),
                ),
            ],
            style={**CARD_STYLE, "marginBottom": "20px"},
        )

    def _viz_card(self) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Span(
                        "Distribution & Prediction Shift",
                        style={"fontWeight": "700", "fontSize": "14px"},
                    )
                ),
                dbc.CardBody(
                    dcc.Loading(html.Div(id="wi-viz"), type="circle"),
                ),
            ],
            style={**CARD_STYLE},
        )

    def content(self) -> html.Div:
        return html.Div(
            [
                self.helper_func.page_header(
                    "What-If Simulation",
                    "Simulate a Feature Across the Test Set and Observe How Model Performance Shifts."
                ),
                self.helper_func.no_data_alert(
                    "wi-no-data-msg", icon_class="bi bi-sliders"
                ),
                html.Div(
                    id="wi-content",
                    style={"display": "none"},
                    children=[
                        self._config_card(),
                        self._metrics_card(),
                        self._viz_card(),
                    ],
                ),
            ]
        )
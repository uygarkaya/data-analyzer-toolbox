from dash import html, dcc
from utils.helpers import HelperFunc
from utils.constants import CARD_STYLE 
from utils.constants import SECTION_DIVIDER_STYLE
import dash_bootstrap_components as dbc

class Explainability:
    def __init__(self) -> None:
        self.helper_func = HelperFunc()

    def _graph_card(self, title: str, graph_id: str) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Span(title, style={"fontWeight": "700", "fontSize": "14px"})
                ),
                dbc.CardBody(
                    dcc.Loading(
                        dcc.Graph(
                            id=graph_id,
                            config={"displayModeBar": False},
                        ),
                        type="circle",
                    )
                ),
            ],
            style={**CARD_STYLE, "marginBottom": "20px"},
        )

    def _meta_pill(self, pill_id: str, accent: str) -> html.Div:
        return html.Div(
            id=pill_id,
            style={
                "display": "inline-flex",
                "alignItems": "center",
                "gap": "6px",
                "padding": "6px 12px",
                "borderRadius": "999px",
                "backgroundColor": "#F8F9FA",
                "border": f"1px solid {accent}33",
                "color": accent,
                "fontSize": "12px",
                "fontWeight": "600",
                "whiteSpace": "nowrap",
            },
        )

    def _local_card(self) -> dbc.Card:
        label = self.helper_func.field_label
        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Span(
                        "Local Explanation",
                        style={"fontWeight": "700", "fontSize": "14px"},
                    )
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        label("Test-set Row Index"),
                                        dbc.Input(
                                            id="explain-row-index",
                                            type="number",
                                            value=0,
                                            min=0,
                                            step=1,
                                            style={"fontSize": "13px"},
                                        ),
                                    ],
                                    md=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            self._meta_pill("explain-row-position", "#0D6EFD"),
                                            self._meta_pill("explain-row-total", "#198754"),
                                        ],
                                        style={
                                            "display": "flex",
                                            "flexWrap": "wrap",
                                            "gap": "8px",
                                            "alignItems": "center",
                                            "height": "100%",
                                            "paddingTop": "22px",
                                        },
                                    ),
                                    md=9,
                                ),
                            ],
                            className="g-2",
                        ),
                        html.Hr(style=SECTION_DIVIDER_STYLE),
                        dcc.Loading(
                            dcc.Graph(
                                id="explain-local-shap",
                                config={"displayModeBar": False},
                                style={"height": "440px"},
                            ),
                            type="circle",
                        ),
                    ]
                ),
            ],
            style={**CARD_STYLE, "marginBottom": "20px"},
        )

    def content(self) -> html.Div:
        return html.Div(
            [
                dcc.Store(id="stored-shap", storage_type="memory"),
                self.helper_func.page_header(
                    "Explainability",
                    "Global Feature Importance and SHAP Attributions on the Test Set.",
                ),
                self.helper_func.no_data_alert(
                    "explain-no-data-msg", icon_class="bi bi-lightbulb"
                ),
                html.Div(
                    id="explain-content",
                    style={"display": "none"},
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.Div(
                                        [
                                            html.Span(
                                                "Trained Model",
                                                style={
                                                    "fontWeight": "700",
                                                    "fontSize": "14px",
                                                    "color": "#1a1a2e",
                                                },
                                            ),
                                            html.Span(
                                                id="explain-model-summary",
                                                style={
                                                    "fontSize": "13px",
                                                    "color": "#495057",
                                                },
                                            ),
                                        ],
                                        style={
                                            "display": "flex",
                                            "justifyContent": "space-between",
                                            "alignItems": "center",
                                            "flexWrap": "wrap",
                                            "gap": "12px",
                                        },
                                    )
                                ),
                                dbc.CardBody(
                                    dbc.Button(
                                        [html.I(className="bi bi-lightbulb me-2"), "Compute Explanations"],
                                        id="explain-compute-btn",
                                        color="primary",
                                        className="w-100",
                                    ),
                                ),
                            ],
                            style={**CARD_STYLE, "marginBottom": "20px"},
                        ),
                        html.Div(
                            id="explain-results",
                            style={"display": "none"},
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            self._graph_card(
                                                "Permutation Importance",
                                                "explain-perm-graph",
                                            ),
                                            md=6,
                                        ),
                                        dbc.Col(
                                            self._graph_card(
                                                "SHAP Global Importance",
                                                "explain-shap-global",
                                            ),
                                            md=6,
                                        ),
                                    ]
                                ),
                                html.Hr(style={"color": "#6C757D", "margin": "-15px 0"}),
                                self._local_card(),
                            ],
                        ),
                    ],
                ),
            ]
        )

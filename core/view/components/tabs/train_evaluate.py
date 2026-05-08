import dash_bootstrap_components as dbc
from dash import html, dcc
from utils.helpers import HelperFunc
from utils.constants import CARD_STYLE, SECTION_DIVIDER_STYLE

class TrainEvaluate:
    def __init__(self) -> None:
        self.helper_func = HelperFunc()

    def _config_card(self) -> dbc.Card:
        label = self.helper_func.field_label
        return self.helper_func.build_card(
            variant="section",
            title="Algorithm & Hyperparameters",
            body=[
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                label("Family"),
                                dcc.Dropdown(
                                    id="train-family",
                                    placeholder="Select Family...",
                                    clearable=False,
                                    style={"marginBottom": "10px"},
                                ),
                            ],
                            md=6,
                        ),
                        dbc.Col(
                            [
                                label("Algorithm"),
                                dcc.Dropdown(
                                    id="train-algorithm",
                                    placeholder="Select Algorithm...",
                                    clearable=False,
                                    style={"marginBottom": "10px"},
                                ),
                            ],
                            md=6,
                        ),
                    ],
                    className="g-2",
                ),
                html.Div(id="train-hyperparams", style={"marginBottom": "16px"}),
                dbc.Button(
                    "Train & Evaluate",
                    id="train-fit-btn",
                    color="success",
                    className="w-100",
                )
            ],
        )

    def _metrics_card(self) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Span(
                        "Baseline Metrics",
                        style={"fontWeight": "700", "fontSize": "14px"},
                    )
                ),
                dbc.CardBody(
                    [
                        dbc.Row(id="train-metric-cards", className="g-3")
                    ]
                ),
            ],
            style={**CARD_STYLE, "marginBottom": "20px"},
        )

    def _diag_col(self, graph_id: str) -> dbc.Col:
        return dbc.Col(
            dcc.Loading(
                dcc.Graph(
                    id=graph_id,
                    config={"displayModeBar": False},
                    style={"height": "340px"},
                ),
                type="circle",
            ),
            md=6,
            style={"marginBottom": "12px"},
        )

    def _diagnostics_card(self) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Span(
                        "Evaluation Metrics",
                        style={"fontWeight": "700", "fontSize": "14px"},
                    )
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                self._diag_col("train-diag-1"),
                                self._diag_col("train-diag-2"),
                            ]
                        ),
                    ]
                ),
            ],
            style={**CARD_STYLE},
        )

    def content(self) -> html.Div:
        return html.Div(
            [
                dcc.Store(id="stored-model", storage_type="memory"),
                dcc.Store(id="stored-metrics", storage_type="memory"),
                self.helper_func.page_header(
                    "Train & Evaluate Model",
                    "Fit a Baseline Model on the Frozen Train Split and Evaluate its Performance.",
                ),
                self.helper_func.no_data_alert(
                    "train-no-data-msg", icon_class="bi bi-cpu"
                ),
                html.Div(
                    id="train-content",
                    style={"display": "none"},
                    children=[
                        dbc.Row(
                            [dbc.Col(self._config_card(), md=12)],
                            className="mb-4",
                        ),
                        html.Div(
                            id="train-results",
                            style={"display": "none"},
                            children=[
                                self._metrics_card(),
                                html.Hr(style=SECTION_DIVIDER_STYLE),
                                self._diagnostics_card(),
                            ],
                        ),
                    ],
                ),
            ]
        )

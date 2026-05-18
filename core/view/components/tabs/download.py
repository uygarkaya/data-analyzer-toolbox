from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.helpers import HelperFunc
from utils.constants import CARD_STYLE, SECTION_DIVIDER_STYLE

class Download:
    def __init__(self) -> None:
        self.helper_func = HelperFunc()

    def _summary_card(self) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Span(
                        "Model Summary",
                        style={"fontWeight": "700", "fontSize": "14px"},
                    )
                ),
                dbc.CardBody(
                    dcc.Loading(html.Div(id="dl-summary"), type="circle"),
                ),
            ],
            style={**CARD_STYLE, "marginBottom": "20px"},
        )

    def _artifact_card(self, title: str, description: str, btn_id: str,
                       btn_label: str, btn_color: str, icon: str) -> dbc.Col:
        return dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.I(
                                    className=f"{icon} me-2",
                                    style={"fontSize": "20px", "color": btn_color},
                                ),
                                html.Span(
                                    title,
                                    style={"fontWeight": "700", "fontSize": "14px", "marginLeft": "-8px"},
                                ),
                            ],
                            style={"marginBottom": "8px"},
                        ),
                        html.Div(
                            description,
                            style={
                                "fontSize": "12px",
                                "color": "#6C757D",
                                "marginBottom": "14px",
                                "minHeight": "36px",
                            },
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-download me-2"), btn_label],
                            id=btn_id,
                            color="primary",
                            outline=True,
                            className="w-100",
                        ),
                    ]
                ),
                style={**CARD_STYLE, "height": "100%"},
            ),
            xs=12, sm=6, md=4,
            style={"marginBottom": "16px"},
        )

    def _downloads_card(self) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Div(
                        [
                            html.Span(
                                "Artifacts",
                                style={"fontWeight": "700", "fontSize": "14px"},
                            ),
                            dbc.Button(
                                html.I(
                                    className="bi bi-download",
                                    style={"fontSize": "16px"},
                                ),
                                id="dl-bundle-btn",
                                color="link",
                                size="sm",
                                title="Download Artifacts Bundle (.zip)",
                                style={
                                    "padding": "0 4px",
                                    "color": "#0D6EFD",
                                    "textDecoration": "none",
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "justifyContent": "space-between",
                            "alignItems": "center",
                        },
                    )
                ),
                dbc.CardBody(
                    dbc.Row(
                        [
                            self._artifact_card(
                                title="Trained Model",
                                description="Serialized Scikit-Learn Pipeline as a Pickle File",
                                btn_id="dl-model-btn",
                                btn_label="Download model.pkl",
                                btn_color="#0D6EFD",
                                icon="bi bi-cpu",
                            ),
                            self._artifact_card(
                                title="Model Card",
                                description="Markdown Report with Algorithm, Hyperparameters, Features, and Test Set Metrics",
                                btn_id="dl-card-btn",
                                btn_label="Download model_card.md",
                                btn_color="#6F42C1",
                                icon="bi bi-file-earmark-text",
                            ),
                            self._artifact_card(
                                title="Cleaned Dataset",
                                description="Post-Cleaning, Post-Feature-Engineering Dataset as CSV",
                                btn_id="dl-data-btn",
                                btn_label="Download dataset.csv",
                                btn_color="#198754",
                                icon="bi bi-table",
                            ),
                        ],
                        className="g-3",
                    )
                ),
            ],
            style={**CARD_STYLE},
        )

    def content(self) -> html.Div:
        return html.Div(
            [
                dcc.Download(id="dl-model-file"),
                dcc.Download(id="dl-card-file"),
                dcc.Download(id="dl-data-file"),
                dcc.Download(id="dl-metrics-file"),
                dcc.Download(id="dl-bundle-file"),
                self.helper_func.page_header(
                    "Download Artifacts",
                    "Export the Trained Model, Model Card, and Supporting Data for Reproduction.",
                ),
                self.helper_func.no_data_alert(
                    "dl-no-data-msg", icon_class="bi bi-cloud-download"
                ),
                html.Div(
                    id="dl-content",
                    style={"display": "none"},
                    children=[
                        self._summary_card(),
                        html.Hr(style=SECTION_DIVIDER_STYLE),
                        self._downloads_card(),
                    ],
                ),
            ]
        )

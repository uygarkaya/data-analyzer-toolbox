import dash_bootstrap_components as dbc
from dash import html, dcc
from utils.helpers import HelperFunc
from utils.constants import CARD_STYLE

class FeatureEngineering:
    def __init__(self):
        self.helper_func = HelperFunc()

    def _target_card(self) -> dbc.Card:
        label = self.helper_func.field_label
        return self.helper_func.build_card(
            variant="section",
            title="Select Target Column",
            body=[
                label("Target Column"),
                dcc.Dropdown(
                    id="fe-target-col",
                    placeholder="Select Target...",
                    clearable=False,
                    style={"marginBottom": "10px"},
                ),
                html.Div(id="fe-task-type-badge", style={"marginBottom": "10px"}),
                label("Exclude Columns"),
                dcc.Dropdown(
                    id="fe-exclude-cols",
                    placeholder="High-cardinality / ID columns...",
                    multi=True,
                    style={"marginBottom": "10px"},
                ),
                html.Div(id="fe-feature-summary", style={"fontSize": "13px", "color": "#6C757D"}),
            ],
        )

    def _encode_card(self) -> dbc.Card:
        label = self.helper_func.field_label
        return self.helper_func.build_card(
            variant="section",
            title="Encode Categorical Features",
            body=[
                label("Column"),
                dcc.Dropdown(
                    id="fe-encode-col",
                    placeholder="Select Categorical Column...",
                    clearable=False,
                    style={"marginBottom": "10px"},
                ),
                label("Encoding Method"),
                dcc.Dropdown(
                    id="fe-encode-method",
                    options=[
                        {"label": "Label Encoding", "value": "label"},
                        {"label": "One-Hot Encoding", "value": "onehot"},
                    ],
                    placeholder="Select Method...",
                    clearable=False,
                    style={"marginBottom": "10px"},
                ),
                html.Div(
                    id="fe-encode-info",
                    style={"fontSize": "12px", "color": "#6C757D", "marginBottom": "45px"},
                ),
                dbc.Button("Apply Encoding", id="fe-encode-btn", color="primary", className="w-100"),
            ],
        )

    def _scale_card(self) -> dbc.Card:
        label = self.helper_func.field_label
        return self.helper_func.build_card(
            variant="section",
            title="Scale Numeric Features",
            body=[
                label("Columns"),
                dcc.Dropdown(
                    id="fe-scale-cols",
                    placeholder="Select Numeric Columns...",
                    multi=True,
                    style={"marginBottom": "10px"},
                ),
                label("Scaler"),
                dcc.Dropdown(
                    id="fe-scale-method",
                    options=[
                        {"label": "Standard Scaler", "value": "standard"},
                        {"label": "MinMax Scaler (0–1 range)", "value": "minmax"},
                    ],
                    placeholder="Select Scaler...",
                    clearable=False,
                    style={"marginBottom": "44px"},
                ),
                dbc.Button("Apply Scaling", id="fe-scale-btn", color="primary", className="w-100"),
            ],
        )

    def _split_card(self) -> dbc.Card:
        label = self.helper_func.field_label
        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Span(
                        "Train / Test Split & K-Fold Cross-Validation",
                        style={"fontWeight": "700", "fontSize": "14px", "display": "block"},
                    )
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        label("Test Size"),
                                        dcc.Slider(
                                            id="fe-test-size",
                                            min=0.1, max=0.4, step=0.05, value=0.2,
                                            marks={v: f"{v:.0%}" for v in [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]},
                                            tooltip={"placement": "bottom", "always_visible": False},
                                        ),
                                    ],
                                    md=5,
                                ),
                                dbc.Col(
                                    [
                                        label("Cross-Validation Folds"),
                                        dbc.Input(
                                            id="fe-cv-folds",
                                            type="number", value=5, min=2, max=10, step=1,
                                            style={"fontSize": "13px"},
                                        ),
                                    ],
                                    md=2,
                                ),
                                dbc.Col(
                                    [
                                        label("Random State"),
                                        dbc.Input(
                                            id="fe-random-state",
                                            type="number", value=42, min=0,
                                            style={"fontSize": "13px"},
                                        ),
                                    ],
                                    md=2,
                                ),
                                dbc.Col(
                                    [
                                        html.Div(style={"height": "24px"}),
                                        dbc.Button(
                                            "Apply Split & Save",
                                            id="fe-split-btn",
                                            color="success",
                                            className="w-100",
                                        ),
                                    ],
                                    md=3,
                                ),
                            ],
                            className="align-items-end",
                        ),
                        html.Div(id="fe-split-summary", style={"marginTop": "12px"}),
                    ]
                ),
            ],
            style={**CARD_STYLE, "marginBottom": "20px"},
        )

    def content(self) -> html.Div:
        return html.Div(
            [
                dcc.Store(id="fe-stored-features", storage_type="memory"),
                self.helper_func.page_header(
                    "Feature Engineering",
                    "Transform and Create New Features for Better Model Performance.",
                ),
                self.helper_func.no_data_alert("fe-no-data-msg", icon_class="bi bi-bar-chart-line"),
                html.Div(
                    id="fe-content",
                    style={"display": "none"},
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(self._target_card(), md=4),
                                dbc.Col(self._encode_card(), md=4),
                                dbc.Col(self._scale_card(), md=4),
                            ],
                            className="mb-4",
                        ),
                        self._split_card(),
                        self.helper_func.preview_card(
                            title="Engineered Features Preview",
                            table_id="fe-preview-table",
                            shape_id="fe-shape-info",
                        ),
                    ],
                ),
            ]
        )

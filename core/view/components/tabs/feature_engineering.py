from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from utils.helpers import HelperFunc
from utils.constants import TABLE_STYLE

class FeatureEngineering:
    def __init__(self):
        self.helper_func = HelperFunc()

    def content(self) -> html.Div:
        return html.Div([
            dcc.Store(id="fe-stored-features", storage_type="memory"),

            html.H4(
                "Feature Engineering",
                style={"fontWeight": "700"}
            ),
            html.H6(
                "Transform and Create New Features for Better Model Performance!",
                style={"color": "#6C757D", "marginBottom": "24px"}
            ),

            self.helper_func.no_data_alert("fe-no-data-msg", icon_class="bi bi-bar-chart-line"),

            html.Div(
                id="fe-content",
                style={"display": "none"},
                children=[
                    dbc.Row([
                        dbc.Col(
                            self.helper_func.build_card(
                                variant="section",
                                title="Select Target Column",
                                body=[
                                    html.Label("Target Column", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dcc.Dropdown(
                                        id="fe-target-col",
                                        placeholder="Select Target...",
                                        clearable=False,
                                        style={"marginBottom": "10px"},
                                    ),
                                    html.Div(
                                        id="fe-task-type-badge",
                                        style={"marginBottom": "10px"},
                                    ),
                                    html.Label("Exclude Columns", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dcc.Dropdown(
                                        id="fe-exclude-cols",
                                        placeholder="High-cardinality / ID columns...",
                                        multi=True,
                                        style={"marginBottom": "10px"},
                                    ),
                                    html.Div(
                                        id="fe-feature-summary",
                                        style={"fontSize": "13px", "color": "#6C757D"},
                                    ),
                                ],
                            ),
                            md=4,
                        ),

                        dbc.Col(
                            self.helper_func.build_card(
                                variant="section",
                                title="Encode Categorical Features",
                                body=[
                                    html.Label("Column", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dcc.Dropdown(
                                        id="fe-encode-col",
                                        placeholder="Select Categorical Column...",
                                        clearable=False,
                                        style={"marginBottom": "10px"},
                                    ),
                                    html.Label("Encoding Method", style={"fontWeight": "600", "fontSize": "13px"}),
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
                            ),
                            md=4,
                        ),

                        dbc.Col(
                            self.helper_func.build_card(
                                variant="section",
                                title="Scale Numeric Features",
                                body=[
                                    html.Label("Columns", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dcc.Dropdown(
                                        id="fe-scale-cols",
                                        placeholder="Select Numeric Columns...",
                                        multi=True,
                                        style={"marginBottom": "10px"},
                                    ),
                                    html.Label("Scaler", style={"fontWeight": "600", "fontSize": "13px"}),
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
                            ),
                            md=4,
                        ),
                    ], className="mb-4"),

                    dbc.Card([
                        dbc.CardHeader(
                            html.Div([
                                html.Span("Train / Test Split & K-Fold Cross-Validation", style={
                                    "fontWeight": "700", "fontSize": "14px", "display": "block",
                                }),
                            ], style={"display": "flex", "alignItems": "center"})
                        ),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Test Size", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dcc.Slider(
                                        id="fe-test-size",
                                        min=0.1, max=0.4, step=0.05, value=0.2,
                                        marks={v: f"{v:.0%}" for v in [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]},
                                        tooltip={"placement": "bottom", "always_visible": False},
                                    ),
                                ], md=5),
                                dbc.Col([
                                    html.Label("Cross-Validation Folds", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dbc.Input(
                                        id="fe-cv-folds",
                                        type="number",
                                        value=5,
                                        min=2,
                                        max=10,
                                        step=1,
                                        style={"fontSize": "13px"},
                                    ),
                                ], md=2),
                                dbc.Col([
                                    html.Label("Random State", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dbc.Input(
                                        id="fe-random-state",
                                        type="number",
                                        value=42,
                                        min=0,
                                        style={"fontSize": "13px"},
                                    ),
                                ], md=2),
                                dbc.Col([
                                    html.Div(style={"height": "24px"}),
                                    dbc.Button(
                                        "Apply Split & Save",
                                        id="fe-split-btn",
                                        color="success",
                                        className="w-100",
                                    ),
                                ], md=3),
                            ], className="align-items-end"),
                            html.Div(id="fe-split-summary", style={"marginTop": "12px"}),
                        ]),
                    ], style={
                        "borderRadius": "10px",
                        "boxShadow": "0 1px 6px rgba(0,0,0,0.07)",
                        "marginBottom": "20px",
                    }),

                    dbc.Card([
                        dbc.CardHeader(
                            html.Div([
                                html.Div([
                                    html.Span("Engineered Features Preview", style={
                                        "fontWeight": "700", "fontSize": "15px", "display": "block",
                                    }),
                                    html.Span(id="fe-shape-info", style={
                                        "fontSize": "12px", "color": "#6C757D",
                                    }),
                                ]),
                            ], style={"display": "flex", "alignItems": "center"})
                        ),
                        dbc.CardBody(
                            dash_table.DataTable(
                                id="fe-preview-table",
                                page_size=10,
                                style_table=TABLE_STYLE["table"],
                                style_header=TABLE_STYLE["header"],
                                style_cell={**TABLE_STYLE["cell"], "fontFamily": "inherit"},
                                style_data_conditional=TABLE_STYLE["striped"],
                            )
                        ),
                    ], style={
                        "borderRadius": "10px",
                        "boxShadow": "0 1px 6px rgba(0,0,0,0.07)",
                    }),
                ],
            ),
        ])

from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from utils.helpers import HelperFunc

class FeatureEngineering:
    def __init__(self):
        self.helper = HelperFunc()

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

            html.Div(
                id="fe-no-data-msg",
                children=dbc.Alert(
                    [
                        html.I(className="bi bi-bar-chart-line me-2"),
                        "No Dataset Loaded Yet. Upload or Select a Sample Dataset to Begin"
                    ],
                    color="danger",
                    style={
                        "borderRadius": "8px",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "height": "80px",
                        "width": "100%"
                    }
                )
            ),

            html.Div(
                id="fe-content",
                style={"display": "none"},
                children=[
                    dbc.Row([
                        dbc.Col(
                            self.helper.data_processing_section_card(
                                "Select Target Column",
                                [
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
                            self.helper.data_processing_section_card(
                                "Encode Categorical Features",
                                [
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
                            self.helper.data_processing_section_card(
                                "Scale Numeric Features",
                                [
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
                                style_table={
                                    "overflowX": "auto",
                                    "borderRadius": "8px",
                                    "border": "1px solid #DEE2E6",
                                },
                                style_header={
                                    "backgroundColor": "#F8F9FA",
                                    "fontWeight": "700",
                                    "fontSize": "12px",
                                    "textTransform": "uppercase",
                                    "letterSpacing": "0.4px",
                                    "color": "#495057",
                                    "borderBottom": "2px solid #DEE2E6",
                                },
                                style_cell={
                                    "fontSize": "13px",
                                    "fontFamily": "inherit",
                                    "textAlign": "left",
                                    "whiteSpace": "normal",
                                    "maxWidth": "200px",
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                },
                                style_data_conditional=[
                                    {"if": {"row_index": "odd"}, "backgroundColor": "#F8F9FA"}
                                ],
                            )
                        ),
                    ], style={
                        "borderRadius": "10px",
                        "boxShadow": "0 1px 6px rgba(0,0,0,0.07)",
                    }),
                ],
            ),
        ])

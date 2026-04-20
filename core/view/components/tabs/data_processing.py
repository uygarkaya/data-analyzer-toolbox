from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from utils.helpers import HelperFunc
from utils.constants import TABLE_STYLE

class DataProcessing:
    def __init__(self) -> None:
        self.helper_func = HelperFunc()

    def content(self) -> html.Div:
        return html.Div(
            [
                html.H4(
                    "Data Cleaning & Processing",
                    style={"fontWeight": "700"}
                ),
                html.H6(
                    "Clean, Transform, and Prepare Your Dataset for Modeling!",
                    style={"color": "#6c757d", "marginBottom": "24px"},
                ),

                self.helper_func.no_data_alert("proc-no-data-msg"),

                html.Div(
                    id="proc-content",
                    style={"display": "none"},
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    self.helper_func.build_card(
                                        variant="section",
                                        title="Handle Missing Values",
                                        body=[
                                            html.Label("Column", style={"fontWeight": "600", "fontSize": "13px"}),
                                            dcc.Dropdown(
                                                id="proc-null-col",
                                                placeholder="Select Column...",
                                                clearable=False,
                                                style={"marginBottom": "10px"},
                                            ),
                                            html.Label("Strategy", style={"fontWeight": "600", "fontSize": "13px"}),
                                            dcc.Dropdown(
                                                id="proc-null-strategy",
                                                options=[
                                                    {"label": "Fill with Mean", "value": "mean"},
                                                    {"label": "Fill with Median", "value": "median"},
                                                    {"label": "Fill with Mode", "value": "mode"},
                                                    {"label": "Fill with Constant", "value": "constant"},
                                                    {"label": "Drop Rows", "value": "drop"},
                                                ],
                                                placeholder="Select Strategy...",
                                                clearable=False,
                                                style={"marginBottom": "10px"},
                                            ),
                                            html.Label("Constant Value", style={"fontWeight": "600", "fontSize": "13px"}),
                                            dbc.Input(
                                                id="proc-null-constant",
                                                placeholder="e.g. 0 or N/A",
                                                type="text",
                                                disabled=True,
                                                style={"fontSize": "13px", "marginBottom": "14px"},
                                            ),
                                            dbc.Button("Apply", id="proc-null-btn", color="primary", className="w-100"),
                                        ],
                                    ),
                                    md=4
                                ),

                                dbc.Col(
                                    self.helper_func.build_card(
                                        variant="section",
                                        title="Remove Duplicate Rows",
                                        body=[
                                            html.Label("Subset Columns (optional)", style={"fontWeight": "600", "fontSize": "13px"}),
                                            dcc.Dropdown(
                                                id="proc-dup-cols",
                                                placeholder="All Columns (default)",
                                                multi=True,
                                                style={"marginBottom": "10px"},
                                            ),
                                            html.Label("Keep", style={"fontWeight": "600", "fontSize": "13px"}),
                                            dcc.Dropdown(
                                                id="proc-dup-keep",
                                                options=[
                                                    {"label": "Keep First Occurrence", "value": "first"},
                                                    {"label": "Keep Last Occurrence", "value": "last"},
                                                    {"label": "Drop All Duplicates", "value": "none"},
                                                ],
                                                value="first",
                                                clearable=False,
                                                style={"marginBottom": "82px"},
                                            ),
                                            dbc.Button("Remove", id="proc-dup-btn", color="primary", className="w-100"),
                                        ],
                                    ),
                                    md=4
                                ),

                                dbc.Col(
                                    self.helper_func.build_card(
                                        variant="section",
                                        title="Rename / Drop Columns",
                                        body=[
                                            html.Label("Column", style={"fontWeight": "600", "fontSize": "13px"}),
                                            dcc.Dropdown(
                                                id="proc-col-select",
                                                placeholder="Select Column...",
                                                clearable=False,
                                                style={"marginBottom": "10px"},
                                            ),
                                            html.Label("New Name", style={"fontWeight": "600", "fontSize": "13px"}),
                                            dbc.Input(
                                                id="proc-col-newname",
                                                placeholder="Enter New Name",
                                                type="text",
                                                style={"fontSize": "13px", "marginBottom": "84px"},
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(dbc.Button("Rename", id="proc-rename-btn", color="primary", className="w-100"), width=6),
                                                    dbc.Col(dbc.Button("Drop", id="proc-drop-btn", color="danger", className="w-100"), width=6),
                                                ],
                                                className="g-2",
                                            ),
                                            html.Div(id="proc-col-preview", style={"marginTop": "12px"}),
                                        ],
                                    ),
                                    md=4
                                ),
                            ],
                            className="mb-4",
                        ),

                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Span("Current Dataset Preview", style={"fontWeight": "700", "fontSize": "15px", "display": "block"}),
                                                    html.Span(id="proc-shape-info", style={"fontSize": "12px", "color": "#6C757D"}),
                                                ]
                                            ),
                                        ],
                                        style={"display": "flex", "alignItems": "center"},
                                    )
                                ),
                                dbc.CardBody(
                                    dash_table.DataTable(
                                        id="proc-preview-table",
                                        page_size=10,
                                        style_table=TABLE_STYLE["table"],
                                        style_header=TABLE_STYLE["header"],
                                        style_cell={**TABLE_STYLE["cell"], "fontFamily": "inherit"},
                                        style_data_conditional=TABLE_STYLE["striped"],
                                    )
                                ),
                            ],
                            style={"borderRadius": "10px", "boxShadow": "0 1px 6px rgba(0,0,0,0.07)"},
                        ),
                    ],
                ),
            ]
        )
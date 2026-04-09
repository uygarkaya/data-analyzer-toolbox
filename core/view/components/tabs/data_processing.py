from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from utils.helpers import HelperFunc

class DataProcessing:
    def __init__(self) -> None:
        self.helper = HelperFunc()

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

                html.Div(
                    id="proc-no-data-msg",
                    children=dbc.Alert(
                        [
                            html.I(className="bi bi-database-x me-2"),
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
                    ),
                ),

                html.Div(
                    id="proc-content",
                    style={"display": "none"},
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    self.helper.data_processing_section_card(
                                        "Handle Missing Values",
                                        [
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
                                    self.helper.data_processing_section_card(
                                        "Remove Duplicate Rows",
                                        [
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
                                    self.helper.data_processing_section_card(
                                        "Rename / Drop Columns",
                                        [
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
                                                style={"fontSize": "13px", "marginBottom": "82px"},
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
                                        style_table={
                                            "overflowX": "auto", 
                                            "borderRadius": "8px", 
                                            "border": "1px solid #DEE2E6"
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
                            ],
                            style={"borderRadius": "10px", "boxShadow": "0 1px 6px rgba(0,0,0,0.07)"},
                        ),
                    ],
                ),
            ]
        )
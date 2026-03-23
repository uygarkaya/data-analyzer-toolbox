from dash import html, dash_table
from utils.helpers import HelperFunc
import dash_bootstrap_components as dbc

class DataOverview:
    def __init__(self) -> None:
        self.helper = HelperFunc()

    def content(self) -> html.Div:
        return html.Div([
            html.H4(
                "Dataset Information & Summary", 
                style={"fontWeight": "700"}
            ),
            html.H6(
                "View Dataset Summary, Data Types, Missing Values, and More!",
                style={"color": "#6c757d", "marginBottom": "24px"}
            ),

            html.Div(
                id="overview-no-data-msg",
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
                id="overview-content",
                style={"display": "none"},
                children=[
                    dbc.Row([
                        self.helper.data_overview_stat_card("ov-rows", "Total Rows", "#0D6EFD"),
                        self.helper.data_overview_stat_card("ov-cols", "Total Columns", "#6610F2"),
                        self.helper.data_overview_stat_card("ov-missing", "Missing Values", "#FD7E14"),
                        self.helper.data_overview_stat_card("ov-duplicates", "Duplicate Rows", "#DC3545"),
                        self.helper.data_overview_stat_card("ov-numeric", "Numeric Columns", "#198754"),
                        self.helper.data_overview_stat_card("ov-categorical", "Categorical Cols", "#0DCAF0"),
                        self.helper.data_overview_stat_card("ov-datetime", "Datetime Columns", "#6F42C1"),
                        self.helper.data_overview_stat_card("ov-memory", "Memory Usage", "#20C997"),
                    ], className="g-3", style={"marginBottom": "28px"}),

                    html.H5(
                        "Column Details", 
                        style={
                            "fontWeight": "600", 
                            "marginBottom": "12px"
                        }
                    ),
                    dash_table.DataTable(
                        id="ov-column-table",
                        columns=[
                            {"name": "Column", "id": "column"},
                            {"name": "Data Type", "id": "dtype"},
                            {"name": "Non-Null Count", "id": "non_null"},
                            {"name": "Null Count", "id": "null_count"},
                            {"name": "Null %", "id": "null_pct"},
                            {"name": "Unique Values", "id": "unique"},
                            {"name": "Sample Value", "id": "sample"},
                        ],
                        data=[],
                        page_size=12,
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
                            "borderBottom": "2px solid #DEE2E6"
                        },
                        style_cell={
                            "fontSize": "13px",
                            "padding": "10px 14px",
                            "fontFamily": "sans-serif",
                            "textAlign": "left",
                            "whiteSpace": "normal",
                            "maxWidth": "200px",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis"
                        },
                        style_data_conditional=[
                            {"if": {"row_index": "odd"}, "backgroundColor": "#F8F9FA"},
                            {
                                "if": {"filter_query": "{null_count} > 0", "column_id": "null_count"},
                                "color": "#DC3545",
                                "fontWeight": "600"
                            }
                        ]
                    )
                ]
            )
        ])
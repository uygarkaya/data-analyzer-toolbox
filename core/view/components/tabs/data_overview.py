from dash import html, dash_table
from utils.helpers import HelperFunc
from utils.constants import TABLE_STYLE
import dash_bootstrap_components as dbc

class DataOverview:
    def __init__(self) -> None:
        self.helper_func = HelperFunc()

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

            self.helper_func.no_data_alert("overview-no-data-msg"),

            html.Div(
                id="overview-content",
                style={"display": "none"},
                children=[
                    dbc.Row([
                        self.helper_func.build_card("stat", "Total Rows", "ov-rows", "#0D6EFD"),
                        self.helper_func.build_card("stat", "Total Columns", "ov-cols", "#6610F2"),
                        self.helper_func.build_card("stat", "Missing Values", "ov-missing", "#FD7E14"),
                        self.helper_func.build_card("stat", "Duplicate Rows", "ov-duplicates", "#DC3545"),
                        self.helper_func.build_card("stat", "Numeric Columns", "ov-numeric", "#198754"),
                        self.helper_func.build_card("stat", "Categorical Cols", "ov-categorical", "#0DCAF0"),
                        self.helper_func.build_card("stat", "Datetime Columns", "ov-datetime", "#6F42C1"),
                        self.helper_func.build_card("stat", "Memory Usage", "ov-memory", "#20C997"),
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
                        style_table=TABLE_STYLE["table"],
                        style_header=TABLE_STYLE["header"],
                        style_cell=TABLE_STYLE["cell"],
                        style_data_conditional=TABLE_STYLE["striped"] + [
                            {
                                "if": {"filter_query": "{null_count} > 0", "column_id": "null_count"},
                                "color": "#DC3545",
                                "fontWeight": "600"
                            }
                        ]
                    ),

                    html.H5(
                        "Numeric Summary Statistics",
                        style={
                            "fontWeight": "600",
                            "marginBottom": "12px",
                            "marginTop": "28px"
                        }
                    ),
                    html.Div(
                        id="ov-numeric-summary-wrapper",
                        children=dash_table.DataTable(
                            id="ov-numeric-table",
                            columns=[],
                            data=[],
                            page_size=10,
                            style_table=TABLE_STYLE["table"],
                            style_header=TABLE_STYLE["header"],
                            style_cell={
                                "fontSize": "13px",
                                "fontFamily": "sans-serif",
                                "textAlign": "left"
                            },
                            style_data_conditional=TABLE_STYLE["striped"],
                        )
                    ),
                ]
            )
        ])
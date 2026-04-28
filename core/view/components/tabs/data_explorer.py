import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from utils.helpers import HelperFunc
from utils.constants import (
    TABLE_STYLE,
    CARD_STYLE,
    SECTION_DIVIDER_STYLE,
    INNER_TAB_STYLE,
    INNER_TAB_SELECTED_STYLE,
)

class DataExplorer:
    def __init__(self) -> None:
        self.helper_func = HelperFunc()

    def _fetch_section(self) -> html.Div:
        tab_options = [
            ("DATASETS", "fetch-data-sample"),
            ("FETCH FROM API", "fetch-data-api"),
        ]
        return html.Div(
            [
                self.helper_func.page_header(
                    "Fetch & Load Dataset",
                    "Load a Dataset, or Fetch From an API Endpoint.",
                ),
                dbc.Card(
                    [
                        dbc.CardHeader(
                            dcc.Tabs(
                                id="fetch-data-tabs",
                                value="fetch-data-sample",
                                children=[
                                    dcc.Tab(
                                        label=label,
                                        value=value,
                                        style=INNER_TAB_STYLE,
                                        selected_style=INNER_TAB_SELECTED_STYLE,
                                    )
                                    for label, value in tab_options
                                ],
                                parent_style={"height": "38px"},
                            )
                        ),
                        dbc.CardBody(html.Div(id="fetch-data-tab-content")),
                    ],
                    style=CARD_STYLE,
                ),
            ],
            style={"display": "flex", "flexDirection": "column", "gap": "10px", "width": "100%"},
        )

    def _info_section(self) -> html.Div:
        stat_cards = [
            ("Total Rows", "ov-rows", "#0D6EFD"),
            ("Total Columns", "ov-cols", "#6610F2"),
            ("Missing Values", "ov-missing", "#FD7E14"),
            ("Duplicate Rows", "ov-duplicates", "#DC3545"),
            ("Numeric Columns", "ov-numeric", "#198754"),
            ("Categorical Cols", "ov-categorical", "#0DCAF0"),
            ("Datetime Columns", "ov-datetime", "#6F42C1"),
            ("Memory Usage", "ov-memory", "#20C997"),
        ]
        return html.Div(
            [
                self.helper_func.page_header(
                    "Dataset Information & Summary",
                    "View Dataset Summary, Data Types, Missing Values, and More.",
                ),
                self.helper_func.no_data_alert("overview-no-data-msg"),
                html.Div(
                    id="overview-content",
                    style={"display": "none"},
                    children=[
                        dbc.Row(
                            [
                                self.helper_func.build_card("stat", title, cid, color)
                                for title, cid, color in stat_cards
                            ],
                            className="g-3",
                            style={"marginBottom": "28px"},
                        ),
                        html.H5("Column Details", style={"fontWeight": "600", "marginBottom": "12px"}),
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
                            style_data_conditional=TABLE_STYLE["striped"]
                            + [
                                {
                                    "if": {"filter_query": "{null_count} > 0", "column_id": "null_count"},
                                    "color": "#DC3545",
                                    "fontWeight": "600",
                                }
                            ],
                        ),
                        html.H5(
                            "Numeric Summary Statistics",
                            style={"fontWeight": "600", "marginBottom": "12px", "marginTop": "28px"},
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
                                style_cell={**TABLE_STYLE["cell"], "fontFamily": "inherit"},
                                style_data_conditional=TABLE_STYLE["striped"],
                            ),
                        ),
                    ],
                ),
            ]
        )

    def _eda_section(self) -> html.Div:
        chart_cards = [
            ("Distribution — Histogram", "eda-histogram"),
            ("Correlation Heatmap", "eda-heatmap"),
            ("Box Plot — Outlier Detection", "eda-boxplot"),
            ("Top Categorical Value Counts", "eda-barchart"),
        ]
        return html.Div(
            [
                self.helper_func.page_header(
                    "Exploratory Data Analysis",
                    "Dive Deeper Into Your Data with Visualizations and Insights.",
                ),
                self.helper_func.no_data_alert("eda-no-data-msg", icon_class="bi bi-bar-chart-line"),
                html.Div(
                    id="eda-content",
                    style={"display": "none"},
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        self.helper_func.field_label("Numeric Column"),
                                        dcc.Dropdown(
                                            id="eda-numeric-col",
                                            placeholder="select a numeric column...",
                                            clearable=False,
                                            style={"fontSize": "13px", "fontFamily": "sans-serif"},
                                        ),
                                    ],
                                    md=6,
                                ),
                                dbc.Col(
                                    [
                                        self.helper_func.field_label("Categorical Column"),
                                        dcc.Dropdown(
                                            id="eda-cat-col",
                                            placeholder="select a categorical column...",
                                            clearable=False,
                                            style={"fontSize": "13px", "fontFamily": "sans-serif"},
                                        ),
                                    ],
                                    md=6,
                                ),
                            ],
                            className="g-3",
                            style={"marginBottom": "24px"},
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    self.helper_func.build_card(
                                        variant="chart", title=title, component_id=cid
                                    ),
                                    md=6,
                                )
                                for title, cid in chart_cards
                            ]
                        ),
                    ],
                ),
            ]
        )

    def content(self) -> html.Div:
        return html.Div(
            [
                dcc.Store(id="stored-dataset", storage_type="memory"),
                self._fetch_section(),
                html.Hr(style=SECTION_DIVIDER_STYLE),
                self._info_section(),
                html.Hr(style=SECTION_DIVIDER_STYLE),
                self._eda_section(),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "gap": "10px",
                "width": "100%",
                "padding": "8px 4px",
            },
        )

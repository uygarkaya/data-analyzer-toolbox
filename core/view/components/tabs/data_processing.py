from dash import html, dcc
from utils.helpers import HelperFunc
import dash_bootstrap_components as dbc

class DataProcessing:
    def __init__(self) -> None:
        self.helper_func = HelperFunc()

    def _null_card(self) -> dbc.Card:
        label = self.helper_func.field_label
        return self.helper_func.build_card(
            variant="section",
            title="Handle Missing Values",
            body=[
                label("Column"),
                dcc.Dropdown(
                    id="proc-null-col",
                    placeholder="Select Column...",
                    clearable=False,
                    style={"marginBottom": "10px"},
                ),
                label("Strategy"),
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
                label("Constant Value"),
                dbc.Input(
                    id="proc-null-constant",
                    placeholder="e.g. 0 or N/A",
                    type="text",
                    disabled=True,
                    style={"fontSize": "13px", "marginBottom": "14px"},
                ),
                dbc.Button("Apply", id="proc-null-btn", color="primary", className="w-100"),
            ],
        )

    def _duplicate_card(self) -> dbc.Card:
        label = self.helper_func.field_label
        return self.helper_func.build_card(
            variant="section",
            title="Remove Duplicate Rows",
            body=[
                label("Subset Columns (optional)"),
                dcc.Dropdown(
                    id="proc-dup-cols",
                    placeholder="All Columns (default)",
                    multi=True,
                    style={"marginBottom": "10px"},
                ),
                label("Keep"),
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
        )

    def _rename_drop_card(self) -> dbc.Card:
        label = self.helper_func.field_label
        return self.helper_func.build_card(
            variant="section",
            title="Rename / Drop Columns",
            body=[
                label("Column"),
                dcc.Dropdown(
                    id="proc-col-select",
                    placeholder="Select Column...",
                    clearable=False,
                    style={"marginBottom": "10px"},
                ),
                label("New Name"),
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
        )

    def content(self) -> html.Div:
        return html.Div(
            [
                self.helper_func.page_header(
                    "Data Cleaning & Processing",
                    "Clean, Transform, and Prepare Your Dataset for Modeling.",
                ),
                self.helper_func.no_data_alert("proc-no-data-msg"),
                html.Div(
                    id="proc-content",
                    style={"display": "none"},
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(self._null_card(), md=4),
                                dbc.Col(self._duplicate_card(), md=4),
                                dbc.Col(self._rename_drop_card(), md=4),
                            ],
                            className="mb-4",
                        ),
                        self.helper_func.preview_card(
                            title="Current Dataset Preview",
                            table_id="proc-preview-table",
                            shape_id="proc-shape-info",
                        ),
                    ],
                ),
            ]
        )
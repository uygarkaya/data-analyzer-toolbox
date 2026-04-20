from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.helpers import HelperFunc

class ExploratoryDataAnalysis:
    def __init__(self) -> None:
        self.helper_func = HelperFunc()

    def content(self) -> html.Div:
        return html.Div([
            html.H4(
                "Exploratory Data Analysis",
                style={"fontWeight": "700"}
            ),
            html.H6(
                "Dive Deeper into Your Data with Visualizations and Insights!",
                style={"color": "#6C757D", "marginBottom": "24px"}
            ),

            self.helper_func.no_data_alert("eda-no-data-msg", icon_class="bi bi-bar-chart-line"),

            html.Div(
                id="eda-content",
                style={"display": "none"},
                children=[
                    dbc.Row([
                        dbc.Col([
                            html.Label("Numeric Column", style={"fontWeight": "600", "fontSize": "13px"}),
                            dcc.Dropdown(
                                id="eda-numeric-col",
                                placeholder="select a numeric column...",
                                clearable=False,
                                style={"fontSize": "13px", "font-family": "sans-serif"}
                            )
                        ], md=6),
                        dbc.Col([
                            html.Label("Categorical Column", style={"fontWeight": "600", "fontSize": "13px"}),
                            dcc.Dropdown(
                                id="eda-cat-col",
                                placeholder="select a categorical column...",
                                clearable=False,
                                style={"fontSize": "13px", "font-family": "sans-serif"}
                            )
                        ], md=6)
                    ], className="g-3", style={"marginBottom": "24px"}),

                    dbc.Row([
                        dbc.Col(self.helper_func.build_card(variant="chart", title="Distribution — Histogram", component_id="eda-histogram"), md=6),
                        dbc.Col(self.helper_func.build_card(variant="chart", title="Correlation Heatmap", component_id="eda-heatmap"), md=6),
                    ]),
                    dbc.Row([ 
                        dbc.Col(self.helper_func.build_card(variant="chart", title="Box Plot — Outlier Detection", component_id="eda-boxplot"), md=6), 
                        dbc.Col(self.helper_func.build_card(variant="chart", title="Top Categorical Value Counts", component_id="eda-barchart"), md=6), 
                    ]),
                ]
            )
        ])
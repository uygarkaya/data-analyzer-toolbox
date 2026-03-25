from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.helpers import HelperFunc

class ExploratoryDataAnalysis:
    def __init__(self) -> None:
        self.helper = HelperFunc()

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

            html.Div(
                id="eda-no-data-msg",
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
                        dbc.Col(self.helper.eda_chart_card("Distribution — Histogram", "eda-histogram"), md=6),
                        dbc.Col(self.helper.eda_chart_card("Correlation Heatmap", "eda-heatmap"), md=6),
                    ]),
                    dbc.Row([ 
                        dbc.Col(self.helper.eda_chart_card("Box Plot — Outlier Detection", "eda-boxplot"), md=6), 
                        dbc.Col(self.helper.eda_chart_card("Top Categorical Value Counts", "eda-barchart"), md=6), 
                    ]),
                ]
            )
        ])
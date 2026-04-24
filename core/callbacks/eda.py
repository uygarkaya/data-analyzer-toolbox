from dash import Output, Input
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from core.view.data_analyzer_toolbox import DataAnalyzerToolbox
from utils.dataframe import HIDDEN, VISIBLE, dropdown_options
from utils.constants import CHART_LAYOUT
ACCENT_COLOR = "#0D6EFD"

class EdaCallbacks:
    def __init__(self, view: DataAnalyzerToolbox) -> None:
        self.view = view

    def register_callbacks(self):
        @self.view.app.callback(
            Output("eda-no-data-msg", "style"),
            Output("eda-content", "style"),
            Output("eda-numeric-col", "options"),
            Output("eda-numeric-col", "value"),
            Output("eda-cat-col", "options"),
            Output("eda-cat-col", "value"),
            Input("stored-dataset", "data"),
            prevent_initial_call=True
        )
        def init_eda_dropdowns(records):
            if not records:
                return VISIBLE, HIDDEN, [], None, [], None

            df = pd.DataFrame(records)
            num_cols = df.select_dtypes(include="number").columns.tolist()
            cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

            return (
                HIDDEN, VISIBLE,
                dropdown_options(num_cols), (num_cols[0] if num_cols else None),
                dropdown_options(cat_cols), (cat_cols[0] if cat_cols else None),
            )

        @self.view.app.callback(
            Output("eda-histogram", "figure"),
            Input("stored-dataset", "data"),
            Input("eda-numeric-col", "value"),
            prevent_initial_call=True
        )
        def update_histogram(records, col):
            if not records or not col:
                return go.Figure()

            df = pd.DataFrame(records)
            fig = px.histogram(
                df,
                x=col,
                nbins=40,
                color_discrete_sequence=[ACCENT_COLOR],
                template="plotly_white"
            )
            fig.update_layout(
                **CHART_LAYOUT,
                bargap=0.05,
                xaxis_title=col,
                yaxis_title="Count",
            )
            return fig

        @self.view.app.callback(
            Output("eda-heatmap", "figure"),
            Input("stored-dataset", "data"),
            prevent_initial_call=True
        )
        def update_heatmap(records):
            if not records:
                return go.Figure()

            df = pd.DataFrame(records)
            num_df = df.select_dtypes(include="number")
            if num_df.shape[1] < 2:
                fig = go.Figure()
                fig.add_annotation(
                    text="Need at Least 2 Numeric Columns",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    font=dict(size=14)
                )
                return fig

            corr = num_df.corr().round(2)
            fig = go.Figure(go.Heatmap(
                z=corr.values,
                x=corr.columns.tolist(),
                y=corr.columns.tolist(),
                colorscale="RdBu",
                zmid=0,
                text=corr.values.round(2),
                texttemplate="%{text}",
                hoverongaps=False
            ))
            fig.update_layout(**CHART_LAYOUT)
            return fig

        @self.view.app.callback(
            Output("eda-boxplot", "figure"),
            Input("stored-dataset", "data"),
            Input("eda-numeric-col", "value"),
            prevent_initial_call=True
        )
        def update_boxplot(records, col):
            if not records or not col:
                return go.Figure()

            df  = pd.DataFrame(records)
            fig = px.box(
                df,
                y=col,
                color_discrete_sequence=[ACCENT_COLOR],
                template="plotly_white",
                points="outliers"
            )
            fig.update_layout(**CHART_LAYOUT)
            return fig

        @self.view.app.callback(
            Output("eda-barchart", "figure"),
            Input("stored-dataset", "data"),
            Input("eda-cat-col", "value"),
            prevent_initial_call=True
        )
        def update_barchart(records, col):
            if not records or not col:
                return go.Figure()

            df = pd.DataFrame(records)
            counts = df[col].value_counts().nlargest(20).reset_index()
            counts.columns = [col, "count"]
            fig = px.bar(
                counts,
                x=col,
                y="count",
                color_discrete_sequence=[ACCENT_COLOR],
                template="plotly_white"
            )
            fig.update_layout(
                **CHART_LAYOUT,
                xaxis_title=col,
                yaxis_title="Count",
                xaxis_tickangle=-35,
            )
            return fig

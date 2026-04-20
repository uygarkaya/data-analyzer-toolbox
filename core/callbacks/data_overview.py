from dash import Output, Input
import pandas as pd

from core.view.dataset_analyzer_toolbox import DatasetAnalyzerToolbox
from utils.dataframe import HIDDEN, VISIBLE

class DataOverviewCallbacks:
    def __init__(self, view: DatasetAnalyzerToolbox) -> None:
        self.view = view

    def register_callbacks(self):
        @self.view.app.callback(
            Output("overview-no-data-msg", "style"),
            Output("overview-content", "style"),
            Output("ov-rows","children"),
            Output("ov-cols", "children"),
            Output("ov-missing", "children"),
            Output("ov-duplicates", "children"),
            Output("ov-numeric", "children"),
            Output("ov-categorical", "children"),
            Output("ov-datetime", "children"),
            Output("ov-memory", "children"),
            Output("ov-column-table", "data"),
            Output("ov-numeric-table", "columns"),
            Output("ov-numeric-table", "data"),
            Input("stored-dataset", "data"),
            prevent_initial_call=True
        )
        def update_data_overview(records):
            if not records:
                return VISIBLE, HIDDEN, "—", "—", "—", "—", "—", "—", "—", "—", [], [], []

            df = pd.DataFrame(records)

            total_rows = len(df)
            total_cols = len(df.columns)
            total_missing = int(df.isnull().sum().sum())
            duplicates = int(df.duplicated().sum())
            numeric_cols = len(df.select_dtypes(include="number").columns)
            cat_cols = len(df.select_dtypes(include=["object", "category"]).columns)
            dt_cols = len(df.select_dtypes(include=["datetime", "datetimetz"]).columns)
            memory_bytes = df.memory_usage(deep=True).sum()
            memory_str = (f"{memory_bytes / 1024:.1f} KB" if memory_bytes < 1_048_576
                            else f"{memory_bytes / 1_048_576:.2f} MB")

            col_rows = []
            for col in df.columns:
                null_count = int(df[col].isnull().sum())
                col_rows.append({
                    "column": col,
                    "dtype": str(df[col].dtype),
                    "non_null": total_rows - null_count,
                    "null_count": null_count,
                    "null_pct": f"{null_count / total_rows * 100:.1f}%",
                    "unique": int(df[col].nunique(dropna=False)),
                    "sample":str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else "N/A",
                })

            num_df = df.select_dtypes(include="number")
            if not num_df.empty:
                desc = num_df.describe().round(4).reset_index().rename(columns={"index": "Statistic"})
                num_columns = [{"name": c, "id": c} for c in desc.columns]
                num_data    = desc.to_dict("records")
            else:
                num_columns, num_data = [], []

            return (
                HIDDEN, VISIBLE,
                f"{total_rows:,}", f"{total_cols:,}",
                f"{total_missing:,}", f"{duplicates:,}",
                str(numeric_cols), str(cat_cols),
                str(dt_cols), memory_str,
                col_rows,
                num_columns, num_data
            )

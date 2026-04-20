from dash import Output, Input, State
from dash import ctx
import pandas as pd

from core.view.dataset_analyzer_toolbox import DatasetAnalyzerToolbox
from utils.helpers import HelperFunc
from utils.dataframe import (
    HIDDEN, VISIBLE, dropdown_options, table_columns, shape_label, preview_data,
)

class DataProcessingCallbacks:
    def __init__(self, view: DatasetAnalyzerToolbox) -> None:
        self.view = view
        self.helper_func_func = HelperFunc()

    def register_callbacks(self):
        @self.view.app.callback(
            Output("proc-no-data-msg", "style"),
            Output("proc-content", "style"),
            Output("proc-null-col", "options"),
            Output("proc-dup-cols", "options"),
            Output("proc-col-select", "options"),
            Output("proc-preview-table", "columns"),
            Output("proc-preview-table", "data"),
            Output("proc-shape-info", "children"),
            Input("stored-dataset", "data"),
            prevent_initial_call=True
        )
        def init_processing(records):
            if not records:
                return VISIBLE, HIDDEN, [], [], [], [], [], ""
            df      = pd.DataFrame(records)
            options = dropdown_options(df.columns)
            cols    = table_columns(df)
            return HIDDEN, VISIBLE, options, options, options, cols, preview_data(df), shape_label(df)

        @self.view.app.callback(
            Output("proc-null-constant", "disabled"),
            Input("proc-null-strategy",  "value"),
            prevent_initial_call=True
        )
        def toggle_constant_input(strategy):
            return strategy != "constant"

        @self.view.app.callback(
            Output("stored-dataset", "data", allow_duplicate=True),
            Output("proc-preview-table", "columns", allow_duplicate=True),
            Output("proc-preview-table", "data", allow_duplicate=True),
            Output("proc-shape-info", "children", allow_duplicate=True),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input("proc-null-btn", "n_clicks"),
            State("stored-dataset", "data"),
            State("proc-null-col", "value"),
            State("proc-null-strategy", "value"),
            State("proc-null-constant", "value"),
            prevent_initial_call=True
        )
        def apply_null_handling(n_clicks, records, col, strategy, constant):
            if not n_clicks or not records or not col or not strategy:
                return records, [], [], "", None
            df = pd.DataFrame(records)
            before = int(df[col].isnull().sum())
            if before == 0:
                msg = self.helper_func_func.generate_alert(f"'{col}' has no Missing Values", color="info")
                return df.to_dict("records"), table_columns(df), preview_data(df), shape_label(df), msg
            try:
                if strategy == "mean":
                    df[col] = df[col].fillna(df[col].mean())
                elif strategy == "median":
                    df[col] = df[col].fillna(df[col].median())
                elif strategy == "mode":
                    df[col] = df[col].fillna(df[col].mode()[0])
                elif strategy == "constant":
                    fill_val = constant if constant not in (None, "") else "0"
                    try:
                        fill_val = float(fill_val) if "." in str(fill_val) else int(fill_val)
                    except ValueError:
                        pass
                    df[col] = df[col].fillna(fill_val)
                elif strategy == "drop":
                    df = df.dropna(subset=[col])
                after  = int(df[col].isnull().sum())
                filled = before - after
                msg    = self.helper_func_func.generate_alert(
                    f"'{col}': {filled} Null(s) Handled Using '{strategy}'. Remaining Nulls: {after}",
                    color="success"
                )
            except Exception as e:
                msg = self.helper_func_func.generate_alert(f"Error: {str(e)}", color="danger")
            return df.to_dict("records"), table_columns(df), preview_data(df), shape_label(df), msg

        @self.view.app.callback(
            Output("stored-dataset", "data", allow_duplicate=True),
            Output("proc-preview-table", "columns", allow_duplicate=True),
            Output("proc-preview-table", "data", allow_duplicate=True),
            Output("proc-shape-info", "children", allow_duplicate=True),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input("proc-dup-btn", "n_clicks"),
            State("stored-dataset", "data"),
            State("proc-dup-cols", "value"),
            State("proc-dup-keep", "value"),
            prevent_initial_call=True
        )
        def apply_remove_duplicates(n_clicks, records, subset, keep):
            if not n_clicks or not records:
                return records, [], [], "", None
            df     = pd.DataFrame(records)
            before = len(df)
            try:
                subset_arg = subset if subset else None
                keep_arg   = False if keep == "none" else keep
                df         = df.drop_duplicates(subset=subset_arg, keep=keep_arg)
                removed    = before - len(df)
                msg = self.helper_func_func.generate_alert(
                    f"Removed {removed} Duplicate Row(s)! Dataset Now has {len(df):,} Rows",
                    color="success" if removed > 0 else "info"
                )
            except Exception as e:
                msg = self.helper_func_func.generate_alert(f"Error: {str(e)}", color="danger")
            return df.to_dict("records"), table_columns(df), preview_data(df), shape_label(df), msg

        @self.view.app.callback(
            Output("stored-dataset", "data", allow_duplicate=True),
            Output("proc-preview-table", "columns", allow_duplicate=True),
            Output("proc-preview-table", "data", allow_duplicate=True),
            Output("proc-shape-info", "children", allow_duplicate=True),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Output("proc-null-col", "options", allow_duplicate=True),
            Output("proc-dup-cols", "options", allow_duplicate=True),
            Output("proc-col-select", "options", allow_duplicate=True),
            Input("proc-rename-btn", "n_clicks"),
            Input("proc-drop-btn", "n_clicks"),
            State("stored-dataset", "data"),
            State("proc-col-select", "value"),
            State("proc-col-newname", "value"),
            prevent_initial_call=True
        )
        def apply_rename_or_drop(rename_clicks, drop_clicks, records, col, new_name):
            if not records or not col:
                return records, [], [], "", None, [], [], []
            df      = pd.DataFrame(records)
            trigger = ctx.triggered_id
            try:
                if trigger == "proc-rename-btn":
                    if not new_name or not new_name.strip():
                        msg = self.helper_func_func.generate_alert("Please Enter a New Column Name!", color="warning")
                    elif new_name.strip() in df.columns:
                        msg = self.helper_func_func.generate_alert(f"Column '{new_name.strip()}' Already Exists.", color="warning")
                    else:
                        df.rename(columns={col: new_name.strip()}, inplace=True)
                        msg = self.helper_func_func.generate_alert(f"'{col}' Renamed to '{new_name.strip()}'.", color="success")
                elif trigger == "proc-drop-btn":
                    df.drop(columns=[col], inplace=True)
                    msg = self.helper_func_func.generate_alert(
                        f"Column '{col}' Dropped! {len(df.columns)} Column(s) Remaining",
                        color="success"
                    )
                else:
                    return records, [], [], "", None, [], [], []
            except Exception as e:
                msg = self.helper_func_func.generate_alert(f"Error: {str(e)}", color="danger")

            options = dropdown_options(df.columns)
            return df.to_dict("records"), table_columns(df), preview_data(df), shape_label(df), msg, options, options, options

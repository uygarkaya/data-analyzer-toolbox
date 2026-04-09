from dash import Output, Input
from dash import ctx, ALL, State
import pandas as pd
import base64, io, requests
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

from core.api.dataset import DatasetAPI
from core.view.dataset_analyzer_toolbox import DatasetAnalyzerToolbox
from utils.notification import Notification

class CoreCallbacks:
    def __init__(self, view: DatasetAnalyzerToolbox) -> None:
        self.view = view
        self.notification = Notification()

    def register_callbacks(self):
        @self.view.app.callback(
            Output("stored-dataset", "data", allow_duplicate=True),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input("upload-dataset", "contents"),
            prevent_initial_call=True
        )
        def store_uploaded_dataset(contents):
            if contents is None:
                return None, None

            content_type, content_string = contents.split(",")
            if "csv" not in content_type:
                alert = self.notification.generate_alert(
                    "Unsupported File Format! Please Upload a CSV File",
                    color="danger"
                )
                return None, alert

            try:
                decoded = base64.b64decode(content_string)
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

                alert = self.notification.generate_alert(
                    "Dataset Uploaded Successfully!",
                    color="success"
                )
                

                return df.to_dict("records"), alert

            except Exception as e:
                alert = self.notification.generate_alert(
                    f"Error Reading File: {str(e)}",
                    color="danger"
                )
                return None, alert
            
        @self.view.app.callback(
            Output("stored-dataset", "data", allow_duplicate=True),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input({"type": "sample-dataset-btn", "index": ALL}, "n_clicks"),
            prevent_initial_call=True
        )
        def load_sample_dataset(n_clicks_list):
            if not any(n_clicks_list):
                return None, None

            triggered_id = ctx.triggered_id
            dataset_id = triggered_id["index"]

            df, entry, error = DatasetAPI.download_dataset(dataset_id)

            if error:
                return None, self.notification.generate_alert(f"Error: {error}", color="danger")

            return df.to_dict("records"), self.notification.generate_alert(
                f"{entry['name']} Loaded Successfully!",
                color="success"
            )
        
        @self.view.app.callback(
            Output("stored-dataset", "data", allow_duplicate=True),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input("fetch-api-btn", "n_clicks"),
            Input("api-url", "value"),
            prevent_initial_call=True
        )
        def fetch_dataset_from_api(n_clicks, url):
            if not n_clicks or not url:
                return None, None

            try:
                response = requests.get(url)

                if response.status_code != 200:
                    alert = self.notification.generate_alert(
                        f"Failed to Fetch Data! Status Code: {response.status_code}",
                        color="danger"
                    )
                    return None, alert

                df = pd.read_csv(io.StringIO(response.text))
                alert = self.notification.generate_alert(
                    "Dataset Fetched Successfully from API!",
                    color="success"
                )

                return df.to_dict("records"), alert

            except Exception as e:
                alert = self.notification.generate_alert(
                    f"Error Fetching API Data: {str(e)}",
                    color="danger"
                )
                return None, alert

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
            HIDDEN  = {"display": "none"}
            VISIBLE = {"display": "block"}

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
            HIDDEN  = {"display": "none"}
            VISIBLE = {"display": "block"}
            if not records:
                return VISIBLE, HIDDEN, [], None, [], None

            df = pd.DataFrame(records)
            num_cols = df.select_dtypes(include="number").columns.tolist()
            cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
            
            return (
                HIDDEN, VISIBLE,
                [{"label": c, "value": c} for c in num_cols], (num_cols[0] if num_cols else None),
                [{"label": c, "value": c} for c in cat_cols], (cat_cols[0] if cat_cols else None),
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
                color_discrete_sequence=["#0D6EFD"], 
                template="plotly_white"
            )
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20), 
                bargap=0.05, 
                xaxis_title=col, 
                yaxis_title="Count",
                font=dict(family="sans-serif")
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
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20), 
                template="plotly_white",
                font=dict(family="sans-serif")
            )
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
                color_discrete_sequence=["#0D6EFD"], 
                template="plotly_white", 
                points="outliers"
            ) 
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                font=dict(family="sans-serif")
            ) 
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
                color_discrete_sequence=["#0D6EFD"], 
                template="plotly_white"
            ) 
            fig.update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis_title=col,
                yaxis_title="Count",
                xaxis_tickangle=-35,
                font=dict(family="sans-serif")
            ) 
            return fig

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
            HIDDEN  = {"display": "none"}
            VISIBLE = {"display": "block"}
            if not records:
                return VISIBLE, HIDDEN, [], [], [], [], [], ""
            df      = pd.DataFrame(records)
            options = [{"label": c, "value": c} for c in df.columns]
            cols    = [{"name": c, "id": c} for c in df.columns]
            shape   = f"{len(df):,} Rows × {len(df.columns)} Columns"
            return HIDDEN, VISIBLE, options, options, options, cols, df.head(20).to_dict("records"), shape

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
                msg = self.notification.generate_alert(f"'{col}' Has No Missing Values", color="info")
                cols  = [{"name": c, "id": c} for c in df.columns]
                return df.to_dict("records"), cols, df.head(20).to_dict("records"), f"{len(df):,} Rows × {len(df.columns)} Columns", msg
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
                msg    = self.notification.generate_alert(
                    f"'{col}': {filled} Null(s) Handled Using '{strategy}'. Remaining Nulls: {after}",
                    color="success"
                )
            except Exception as e:
                msg = self.notification.generate_alert(f"Error: {str(e)}", color="danger")
            cols  = [{"name": c, "id": c} for c in df.columns]
            shape = f"{len(df):,} Rows × {len(df.columns)} Columns"
            return df.to_dict("records"), cols, df.head(20).to_dict("records"), shape, msg

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
                msg = self.notification.generate_alert(
                    f"Removed {removed} Duplicate Row(s)! Dataset Now Has {len(df):,} Rows",
                    color="success" if removed > 0 else "info"
                )
            except Exception as e:
                msg = self.notification.generate_alert(f"Error: {str(e)}", color="danger")
            cols  = [{"name": c, "id": c} for c in df.columns]
            shape = f"{len(df):,} Rows × {len(df.columns)} Columns"
            return df.to_dict("records"), cols, df.head(20).to_dict("records"), shape, msg

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
                        msg = self.notification.generate_alert("Please Enter a New Column Name!", color="warning")
                    elif new_name.strip() in df.columns:
                        msg = self.notification.generate_alert(f"Column '{new_name.strip()}' Already Exists.", color="warning")
                    else:
                        df.rename(columns={col: new_name.strip()}, inplace=True)
                        msg = self.notification.generate_alert(f"'{col}' Renamed to '{new_name.strip()}'.", color="success")
                elif trigger == "proc-drop-btn":
                    df.drop(columns=[col], inplace=True)
                    msg = self.notification.generate_alert(
                        f"Column '{col}' Dropped! {len(df.columns)} Column(s) Remaining",
                        color="success"
                    )
                else:
                    return records, [], [], "", None, [], [], []
            except Exception as e:
                msg = self.notification.generate_alert(f"Error: {str(e)}", color="danger")

            options = [{"label": c, "value": c} for c in df.columns]
            cols = [{"name": c, "id": c} for c in df.columns]
            shape = f"{len(df):,} Rows × {len(df.columns)} Columns"
            return df.to_dict("records"), cols, df.head(20).to_dict("records"), shape, msg, options, options, options
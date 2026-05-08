import pandas as pd
import dash_bootstrap_components as dbc

from dash import Output, Input, State, html
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from core.view.data_analyzer_toolbox import DataAnalyzerToolbox
from utils.helpers import HelperFunc
from utils.dataframe import (
    HIDDEN, VISIBLE, 
    dropdown_options, 
    table_columns, 
    shape_label,
    preview_data, 
    detect_task_type
)

class FeatureEngineeringCallbacks:
    def __init__(self, view: DataAnalyzerToolbox) -> None:
        self.view = view
        self.helper_func_func = HelperFunc()

    def register_callbacks(self):
        @self.view.app.callback(
            Output("fe-no-data-msg", "style"),
            Output("fe-content", "style"),
            Output("fe-target-col", "options"),
            Output("fe-target-col", "value"),
            Output("fe-exclude-cols", "options"),
            Output("fe-encode-col", "options"),
            Output("fe-scale-cols", "options"),
            Output("fe-scale-cols", "value"),
            Output("fe-preview-table", "columns"),
            Output("fe-preview-table", "data"),
            Output("fe-shape-info", "children"),
            Input("stored-dataset", "data"),
            prevent_initial_call=True
        )
        def init_feature_engineering(records):
            if not records:
                return VISIBLE, HIDDEN, [], None, [], [], [], [], [], [], ""

            df = pd.DataFrame(records)
            all_opts = dropdown_options(df.columns)
            cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
            cat_opts = dropdown_options(cat_cols)
            num_cols = df.select_dtypes(include="number").columns.tolist()
            num_opts = dropdown_options(num_cols)
            return (
                HIDDEN, VISIBLE,
                all_opts, None,
                all_opts, cat_opts, num_opts, num_cols,
                table_columns(df), preview_data(df), shape_label(df)
            )

        @self.view.app.callback(
            Output("fe-task-type-badge", "children"),
            Output("fe-feature-summary", "children"),
            Input("fe-target-col", "value"),
            Input("fe-exclude-cols", "value"),
            State("stored-dataset", "data"),
            prevent_initial_call=True
        )
        def update_target_info(target, exclude, records):
            if not records or not target:
                return "", ""

            df = pd.DataFrame(records)
            task_type, color = detect_task_type(df[target])

            badge = dbc.Badge(task_type, color=color, style={"fontSize": "13px", "padding": "6px 12px"})

            excluded = set(exclude or [])
            excluded.add(target)
            feature_count = len([c for c in df.columns if c not in excluded])
            summary = f"{feature_count} Feature Column(s) Selected"

            return badge, summary

        @self.view.app.callback(
            Output("fe-encode-info", "children"),
            Input("fe-encode-col", "value"),
            Input("fe-encode-method", "value"),
            State("stored-dataset", "data"),
            prevent_initial_call=True
        )
        def update_encode_info(col, method, records):
            if not records or not col:
                return ""
            df = pd.DataFrame(records)
            n_unique = df[col].nunique()
            if method == "onehot":
                return f"{n_unique} Unique Values → {n_unique} New Columns"
            elif method == "label":
                return f"{n_unique} Unique Values → Integer 0..{n_unique - 1}"
            return f"{n_unique} Unique Values"

        @self.view.app.callback(
            Output("stored-dataset", "data", allow_duplicate=True),
            Output("fe-preview-table", "columns", allow_duplicate=True),
            Output("fe-preview-table", "data", allow_duplicate=True),
            Output("fe-shape-info", "children", allow_duplicate=True),
            Output("fe-encode-col", "options", allow_duplicate=True),
            Output("fe-scale-cols", "options", allow_duplicate=True),
            Output("fe-scale-cols", "value", allow_duplicate=True),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input("fe-encode-btn", "n_clicks"),
            State("stored-dataset", "data"),
            State("fe-encode-col", "value"),
            State("fe-encode-method", "value"),
            prevent_initial_call=True
        )
        def apply_encoding(n_clicks, records, col, method):
            if not n_clicks or not records or not col or not method:
                return records, [], [], "", [], [], [], None

            df = pd.DataFrame(records)
            try:
                if method == "label":
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
                    mapping = dict(zip(le.classes_, le.transform(le.classes_).tolist()))
                    msg = self.helper_func_func.generate_alert(
                        f"Label Encoded '{col}': {mapping}",
                        color="success"
                    )
                elif method == "onehot":
                    before = df.shape[1]
                    df = pd.get_dummies(df, columns=[col], prefix=[col], drop_first=False, dtype=int)
                    after = df.shape[1]
                    msg = self.helper_func_func.generate_alert(
                        f"One-Hot Encoded '{col}': {before} → {after} Columns (+{after - before} New)",
                        color="success"
                    )
                else:
                    return records, [], [], "", [], [], [], None
            except Exception as e:
                msg = self.helper_func_func.generate_alert(f"Encoding Error: {str(e)}", color="danger")

            cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
            cat_opts = dropdown_options(cat_cols)
            num_cols = df.select_dtypes(include="number").columns.tolist()
            num_opts = dropdown_options(num_cols)
            return df.to_dict("records"), table_columns(df), preview_data(df), shape_label(df), cat_opts, num_opts, num_cols, msg

        @self.view.app.callback(
            Output("stored-dataset", "data", allow_duplicate=True),
            Output("fe-preview-table", "columns", allow_duplicate=True),
            Output("fe-preview-table", "data", allow_duplicate=True),
            Output("fe-shape-info", "children", allow_duplicate=True),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input("fe-scale-btn", "n_clicks"),
            State("stored-dataset", "data"),
            State("fe-scale-cols", "value"),
            State("fe-scale-method", "value"),
            prevent_initial_call=True
        )
        def apply_scaling(n_clicks, records, scale_cols, method):
            if not n_clicks or not records or not scale_cols or not method:
                return records, [], [], "", None

            df = pd.DataFrame(records)
            try:
                scalers = {
                    "standard": StandardScaler,
                    "minmax": MinMaxScaler,
                }
                scaler = scalers[method]()
                df[scale_cols] = scaler.fit_transform(df[scale_cols])
                msg = self.helper_func_func.generate_alert(
                    f"Scaled {len(scale_cols)} Column(s) using {method.title()} Scaler",
                    color="success"
                )
            except Exception as e:
                msg = self.helper_func_func.generate_alert(f"Scaling Error: {str(e)}", color="danger")

            return df.to_dict("records"), table_columns(df), preview_data(df), shape_label(df), msg

        @self.view.app.callback(
            Output("fe-stored-features", "data"),
            Output("fe-split-summary", "children"),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input("fe-split-btn", "n_clicks"),
            State("stored-dataset", "data"),
            State("fe-target-col", "value"),
            State("fe-exclude-cols", "value"),
            State("fe-test-size", "value"),
            State("fe-cv-folds", "value"),
            State("fe-random-state", "value"),
            prevent_initial_call=True
        )
        def apply_split(n_clicks, records, target, exclude, test_size, cv_folds, random_state):
            if not n_clicks or not records or not target:
                return None, "", self.helper_func_func.generate_alert(
                    "Please Select a Target Column First!", color="warning"
                )

            df = pd.DataFrame(records)
            excluded = set(exclude or [])
            excluded.add(target)
            feature_cols = [c for c in df.columns if c not in excluded]

            remaining_cats = df[feature_cols].select_dtypes(include=["object", "category"]).columns.tolist()
            if remaining_cats:
                return None, "", self.helper_func_func.generate_alert(
                    f"Categorical Columns Still Present: {remaining_cats}. Please Encode them First!",
                    color="danger"
                )

            X = df[feature_cols]
            y = df[target]

            if X.isnull().sum().sum() > 0:
                return None, "", self.helper_func_func.generate_alert(
                    f"Features Contain {int(X.isnull().sum().sum())} Missing Value(s). Please Handle them in Data Processing First!",
                    color="danger"
                )

            task_type, _ = detect_task_type(y)

            try:
                from sklearn.model_selection import train_test_split, KFold, StratifiedKFold

                is_classification = task_type in ("Binary Classification", "Multiclass Classification")

                stratify_col = y if is_classification and y.value_counts().min() >= 2 else None
                rs = int(random_state) if random_state is not None else 42
                n_splits = int(cv_folds) if cv_folds is not None else 5
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=rs, stratify=stratify_col
                )

                min_class = int(y_train.value_counts().min()) if is_classification else None
                if is_classification and min_class is not None and n_splits > min_class:
                    return None, "", self.helper_func_func.generate_alert(
                        f"Cross-Validation Folds ({n_splits}) > Smallest Class Size ({min_class}) in Train Set. Reduce Folds!",
                        color="danger"
                    )

                if is_classification:
                    splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=rs)
                else:
                    splitter = KFold(n_splits=n_splits, shuffle=True, random_state=rs)

                y_train_reset = y_train.reset_index(drop=True)
                X_train_reset = X_train.reset_index(drop=True)
                cv_folds_data = []
                for fold_idx, (tr_idx, val_idx) in enumerate(splitter.split(X_train_reset, y_train_reset), start=1):
                    cv_folds_data.append({
                        "fold": fold_idx,
                        "train_idx": tr_idx.tolist(),
                        "val_idx": val_idx.tolist(),
                        "train_size": int(len(tr_idx)),
                        "val_size": int(len(val_idx)),
                    })

                feature_data = {
                    "X_train": X_train_reset.to_dict("records"),
                    "X_test": X_test.to_dict("records"),
                    "y_train": y_train_reset.tolist(),
                    "y_test": y_test.tolist(),
                    "feature_cols": feature_cols,
                    "target_col": target,
                    "task_type": task_type,
                    "test_size": test_size,
                    "cv_folds": n_splits,
                    "cv_strategy": "StratifiedKFold" if is_classification else "KFold",
                    "cv_splits": cv_folds_data,
                    "random_state": rs,
                }

                avg_val = sum(f["val_size"] for f in cv_folds_data) / len(cv_folds_data)
                summary_children = [
                    dbc.Row([
                        dbc.Col(dbc.Badge(f"Task: {task_type}", color="primary", className="me-2", style={"fontSize": "13px", "padding": "6px 12px"}), width="auto"),
                        dbc.Col(dbc.Badge(f"Features: {len(feature_cols)}", color="secondary", className="me-2", style={"fontSize": "13px", "padding": "6px 12px"}), width="auto"),
                        dbc.Col(dbc.Badge(f"Train: {len(X_train):,}", color="success", className="me-2", style={"fontSize": "13px", "padding": "6px 12px"}), width="auto"),
                        dbc.Col(dbc.Badge(f"Test: {len(X_test):,}", color="warning", className="me-2", style={"fontSize": "13px", "padding": "6px 12px"}), width="auto"),
                        dbc.Col(dbc.Badge(f"{feature_data['cv_strategy']}: {n_splits} folds (~{int(avg_val):,} val each)", color="info", style={"fontSize": "13px", "padding": "6px 12px"}), width="auto"),
                    ], className="g-2")
                ]

                msg = self.helper_func_func.generate_alert(
                    f"Split Complete! Train: {len(X_train):,} / Test: {len(X_test):,} ({test_size:.0%}) — {n_splits}-Fold Cross-Validation Ready on Train Set",
                    color="success"
                )
                return feature_data, html.Div(summary_children), msg

            except Exception as e:
                return None, "", self.helper_func_func.generate_alert(
                    f"Split Error: {str(e)}", color="danger"
                )

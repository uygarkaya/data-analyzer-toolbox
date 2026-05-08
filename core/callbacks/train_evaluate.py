import numpy as np
import pandas as pd
import re, pickle, base64
import dash_bootstrap_components as dbc

from sklearn.pipeline import Pipeline
from dash import Input, Output, State, html, no_update, ALL
from core.view.data_analyzer_toolbox import DataAnalyzerToolbox
from utils.constants import METRIC_COLORS, METRIC_LABEL
from utils.dataframe import HIDDEN, VISIBLE
from utils.helpers import HelperFunc
from utils.metrics import compute_with_ci
from utils.figures import diagnostics
from utils.registry import (
    load_model_registry, families_for, algorithms_for,
    find_algorithm, build_params, import_class,
)

def _hyperparam_inputs(registry: dict, algo: dict) -> html.Div:
    field_specs = {f["id"]: f for f in registry["hyperparameter_fields"]}
    rows = []
    for ui in algo.get("ui_fields", []):
        spec = field_specs.get(ui["field"])
        if spec is None:
            continue
        rows.append(dbc.Col([
            html.Label(spec["label"], style={"fontWeight": "600", "fontSize": "12px"}),
            dbc.Input(
                id={"type": "train-hp", "param": ui["param"]},
                type="number", value=spec["default"],
                min=spec.get("min"), step=spec.get("step"),
                style={"fontSize": "13px"},
            ),
        ], md=3))
    if not rows:
        return html.Div(
            "This algorithm has no tunable hyperparameters in the registry.",
            style={"fontSize": "12px", "color": "#6C757D"},
        )
    return dbc.Row(rows, className="g-2")

def _metric_card(name: str, payload: dict) -> dbc.Col:
    color = METRIC_COLORS.get(name, "#0D6EFD")
    return dbc.Col(
        dbc.Card(dbc.CardBody([
            html.Div(METRIC_LABEL.get(name, name), style={
                "fontSize": "11px", "color": "#6C757D", "fontWeight": "600",
                "textTransform": "uppercase", "letterSpacing": "0.5px",
            }),
            html.H4(f"{payload['value']:.3f}", style={
                "fontWeight": "700", "color": color, "marginBottom": "2px",
            }),
        ]), style={"borderLeft": f"4px solid {color}", "borderRadius": "8px"}),
        xs=12, sm=6, md=3,
    )

class TrainEvaluateCallbacks:
    def __init__(self, view: DataAnalyzerToolbox) -> None:
        self.view = view
        self.helper_func = HelperFunc()
        self.registry = load_model_registry()

    def register_callbacks(self):
        registry = self.registry

        @self.view.app.callback(
            Output("train-no-data-msg", "style"),
            Output("train-content", "style"),
            Output("train-family", "options"),
            Output("train-family", "value"),
            Input("fe-stored-features", "data"),
        )
        def init_train(features):
            if not features:
                return VISIBLE, HIDDEN, [], None
            task_label = features.get("task_type", "")
            task = "classification" if "Classification" in task_label else "regression"
            fams = families_for(registry, task)
            return HIDDEN, VISIBLE, fams, (fams[0]["value"] if fams else None)

        @self.view.app.callback(
            Output("train-algorithm", "options"),
            Output("train-algorithm", "value"),
            Input("train-family", "value"),
            State("fe-stored-features", "data"),
            prevent_initial_call=True,
        )
        def update_algorithms(family_value, features):
            if not family_value or not features:
                return [], None
            task_label = features.get("task_type", "")
            task = "classification" if "Classification" in task_label else "regression"
            algos = algorithms_for(registry, family_value, task)
            return algos, (algos[0]["value"] if algos else None)

        @self.view.app.callback(
            Output("train-hyperparams", "children"),
            Input("train-algorithm", "value"),
            State("train-family", "value"),
            prevent_initial_call=True,
        )
        def update_hyperparams(algo_value, family_value):
            if not algo_value or not family_value:
                return ""
            _, algo = find_algorithm(registry, family_value, algo_value)
            return _hyperparam_inputs(registry, algo) if algo else ""

        @self.view.app.callback(
            Output("stored-model", "data"),
            Output("stored-metrics", "data"),
            Output("train-results", "style"),
            Output("train-metric-cards", "children"),
            Output("train-diag-1", "figure"),
            Output("train-diag-2", "figure"),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input("train-fit-btn", "n_clicks"),
            State("fe-stored-features", "data"),
            State("train-family", "value"),
            State("train-algorithm", "value"),
            State({"type": "train-hp", "param": ALL}, "id"),
            State({"type": "train-hp", "param": ALL}, "value"),
            prevent_initial_call=True,
        )
        def train_model(n_clicks, features, family_value, algo_value, hp_ids, hp_values):
            if not n_clicks:
                return (no_update,) * 8
            if not features or not family_value or not algo_value:
                alert = self.helper_func.generate_alert(
                    "Apply a Train/Test split in Feature Engineering first!", color="warning")
                return (no_update,) * 7 + (alert,)

            fam, algo = find_algorithm(registry, family_value, algo_value)
            if algo is None:
                alert = self.helper_func.generate_alert("Algorithm not found in registry.", color="danger")
                return (no_update,) * 7 + (alert,)

            try:
                X_train = pd.DataFrame(features["X_train"])
                X_test = pd.DataFrame(features["X_test"])
                y_train = pd.Series(features["y_train"])
                y_test = pd.Series(features["y_test"])
                feature_cols = features.get("feature_cols") or list(X_train.columns)
                X_train, X_test = X_train[feature_cols], X_test[feature_cols]
                safe_cols = [re.sub(r"[\[\]<>]", "_", str(c)) for c in X_train.columns]
                X_train.columns = X_test.columns = safe_cols

                params = build_params(registry, algo, hp_ids, hp_values)
                pipeline = Pipeline([("estimator", import_class(algo["class"])(**params))])
                pipeline.fit(X_train, y_train)

                task = algo["task"]
                y_pred = pipeline.predict(X_test)
                y_proba = None
                if task == "classification" and algo.get("supports_proba"):
                    try:
                        y_proba = pipeline.predict_proba(X_test)
                    except Exception:
                        y_proba = None

                metrics = compute_with_ci(task, y_test, y_pred, y_proba)
                metric_cols = [_metric_card(n, p) for n, p in metrics.items()]
                d1, d2 = diagnostics(
                    task, y_test, y_pred,
                    np.asarray(y_proba) if y_proba is not None else None,
                )

                model_payload = {
                    "family": family_value, "algorithm": algo_value, "params": params,
                    "task": task, "feature_cols": feature_cols,
                    "target_col": features.get("target_col"),
                    "shap_explainer": fam.get("shap_explainer"),
                    "model_b64": base64.b64encode(pickle.dumps(pipeline)).decode("ascii"),
                }
                metrics_payload = {"task": task, "metrics": metrics}
                alert = self.helper_func.generate_alert(
                    f"Trained {algo['label']} Successfully!", color="success")

                return (model_payload, metrics_payload, {"display": "block"},
                        metric_cols, d1, d2, alert)

            except Exception as e:
                alert = self.helper_func.generate_alert(f"Training Failed: {e}", color="danger")
                return (no_update,) * 7 + (alert,)

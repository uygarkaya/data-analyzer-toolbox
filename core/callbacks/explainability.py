import numpy as np
import pandas as pd
import base64, pickle, re, shap
import plotly.graph_objects as go
from dash import Input, Output, State, html, no_update
from sklearn.inspection import permutation_importance

from utils.constants import CHART_LAYOUT
from utils.dataframe import HIDDEN, VISIBLE
from utils.figures import empty_figure
from utils.helpers import HelperFunc
from core.view.data_analyzer_toolbox import DataAnalyzerToolbox

def _safe_cols(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [re.sub(r"[\[\]<>]", "_", str(c)) for c in df.columns]
    return df

def _bar_figure(names, values) -> go.Figure:
    order = np.argsort(values)
    names = [names[i] for i in order]
    values = [float(values[i]) for i in order]
    fig = go.Figure(data=go.Bar(x=values, y=names, orientation="h", marker_color="#0D6EFD"))
    fig.update_layout(xaxis_title="Importance", yaxis_title="", **CHART_LAYOUT)
    return fig

def _local_waterfall(feature_names, values, row_values, top_k: int = 12) -> go.Figure:
    contribs = np.asarray(values, dtype=float)
    order = np.argsort(np.abs(contribs))[::-1][:top_k]
    names = [f"{feature_names[i]} = {row_values[i]}" for i in order][::-1]
    vals = [float(contribs[i]) for i in order][::-1]
    colors = ["#DC3545" if v < 0 else "#198754" for v in vals]
    fig = go.Figure(data=go.Bar(x=vals, y=names, orientation="h", marker_color=colors))
    fig.update_layout(xaxis_title="SHAP Value (Impact on Prediction)", yaxis_title="", **CHART_LAYOUT)
    return fig

def _select_class_shap(shap_out, class_idx: int = 1):
    """Normalize SHAP output to (values_2d, base_value_scalar) for a chosen class."""
    values, base = shap_out.values, shap_out.base_values
    if values.ndim == 3:
        idx = min(class_idx, values.shape[2] - 1)
        values = values[:, :, idx]
        if np.ndim(base) == 2:
            base = base[:, idx]
    base_scalar = float(np.mean(base)) if np.ndim(base) >= 1 else float(base)
    return values, base_scalar

class ExplainabilityCallbacks:
    def __init__(self, view: DataAnalyzerToolbox) -> None:
        self.view = view
        self.helper_func = HelperFunc()

    def register_callbacks(self):
        @self.view.app.callback(
            Output("explain-no-data-msg", "style"),
            Output("explain-content", "style"),
            Output("explain-model-summary", "children"),
            Input("stored-model", "data"),
            Input("fe-stored-features", "data"),
        )
        def gate(model, features):
            if not model or not features:
                return VISIBLE, HIDDEN, ""

            items = [
                ("Algorithm", str(model.get("algorithm", "?"))),
                ("Test Rows", str(len(features.get("X_test", [])))),
            ]
            sep = html.Span("·", style={"margin": "0 10px", "color": "#CED4DA"})
            children = []
            for i, (label, value) in enumerate(items):
                if i > 0:
                    children.append(sep)
                children.append(html.Span([
                    html.Span(f"{label}: ", style={"color": "#6C757D"}),
                    html.Span(value, style={"fontWeight": "600", "color": "#1a1a2e"}),
                ]))
            return HIDDEN, VISIBLE, children

        @self.view.app.callback(
            Output("stored-shap", "data"),
            Output("explain-results", "style"),
            Output("explain-perm-graph", "figure"),
            Output("explain-shap-global", "figure"),
            Output("explain-row-index", "max"),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input("explain-compute-btn", "n_clicks"),
            State("stored-model", "data"),
            State("fe-stored-features", "data"),
            prevent_initial_call=True,
        )
        def compute_explanations(n_clicks, model, features):
            if not n_clicks or not model or not features:
                return (no_update,) * 6

            try:
                pipeline = pickle.loads(base64.b64decode(model["model_b64"]))
                feature_cols = model.get("feature_cols") or features.get("feature_cols")
                task = model.get("task")
                explainer_kind = (model.get("shap_explainer") or "").lower()

                X_test = _safe_cols(pd.DataFrame(features["X_test"])[feature_cols])
                X_train = _safe_cols(pd.DataFrame(features["X_train"])[feature_cols])
                feat_names = list(X_test.columns)

                perm = permutation_importance(
                    pipeline, X_test, pd.Series(features["y_test"]),
                    n_repeats=5, random_state=42, n_jobs=-1,
                )
                perm_fig = _bar_figure(feat_names, perm.importances_mean)

                estimator = pipeline.named_steps.get("estimator", pipeline)
                X_shap = X_test.iloc[:400]

                if explainer_kind == "tree":
                    explainer = shap.TreeExplainer(estimator)
                elif explainer_kind == "linear":
                    explainer = shap.LinearExplainer(estimator, X_train.iloc[: min(100, len(X_train))])
                else:
                    predict_fn = (
                        estimator.predict_proba
                        if task == "classification" and hasattr(estimator, "predict_proba")
                        else estimator.predict
                    )
                    explainer = shap.KernelExplainer(
                        predict_fn, shap.sample(X_train, min(50, len(X_train)), random_state=42)
                    )
                shap_out = explainer(X_shap)

                shap_vals_2d, base_scalar = _select_class_shap(shap_out, 1 if task == "classification" else 0)
                shap_global_fig = _bar_figure(feat_names, np.mean(np.abs(shap_vals_2d), axis=0))

                stored = {
                    "shap_values_b64": base64.b64encode(pickle.dumps(shap_vals_2d)).decode("ascii"),
                    "base_value": base_scalar,
                    "feature_names": feat_names,
                    "X_shap_records": X_shap.to_dict("records"),
                    "n_explained": len(X_shap),
                    "task": task,
                }
                alert = self.helper_func.generate_alert(
                    f"Computed Explanations on {len(X_shap)} Test Rows.",
                    color="success",
                )
                return (
                    stored,
                    {"display": "block"},
                    perm_fig,
                    shap_global_fig,
                    max(0, len(X_shap) - 1),
                    alert,
                )

            except Exception as e:
                alert = self.helper_func.generate_alert(
                    f"Explanation Failed: {e}", color="danger"
                )
                return (no_update,) * 5 + (alert,)

        @self.view.app.callback(
            Output("explain-local-shap", "figure"),
            Output("explain-row-position", "children"),
            Output("explain-row-total", "children"),
            Input("explain-row-index", "value"),
            Input("stored-shap", "data"),
        )
        def update_local(row_idx, shap_data):
            if not shap_data:
                return empty_figure("Local SHAP", "Compute Explanations First!"), "", ""

            n = shap_data["n_explained"]
            row_idx = int(max(0, min(row_idx or 0, n - 1)))

            shap_vals_2d = pickle.loads(base64.b64decode(shap_data["shap_values_b64"]))
            row_values = list(shap_data["X_shap_records"][row_idx].values())

            fig = _local_waterfall(shap_data["feature_names"], shap_vals_2d[row_idx], row_values)
            total = float(np.sum(shap_vals_2d[row_idx]))
            position_pill = [
                html.I(className="bi bi-eye-fill"),
                html.Span("Showing", style={"opacity": 0.75}),
                html.Span(f"Row {row_idx}", style={"fontWeight": "700"}),
                html.Span("of", style={"opacity": 0.75}),
                html.Span(str(n - 1), style={"fontWeight": "700"}),
            ]
            total_pill = [
                html.I(className="bi bi-graph-up-arrow"),
                html.Span("Total Contribution", style={"opacity": 0.75}),
                html.Span(f"{total:+.3f}", style={"fontWeight": "700"}),
            ]
            return fig, position_pill, total_pill

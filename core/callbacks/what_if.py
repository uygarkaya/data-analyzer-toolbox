import numpy as np
import pandas as pd
import base64, pickle, re
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, callback_context
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_absolute_error, mean_squared_error, r2_score,
)
from core.view.data_analyzer_toolbox import DataAnalyzerToolbox
from utils.dataframe import HIDDEN, VISIBLE
from utils.helpers import HelperFunc

def _safe_cols(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [re.sub(r"[\[\]<>]", "_", str(c)) for c in df.columns]
    return df

def _apply_perturbation(series: pd.Series, pert_type: str, params: dict, rng) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce").astype(float)
    if pert_type == "scale":
        return s * float(params.get("factor", 1.0))
    if pert_type == "noise":
        sigma = float(params.get("sigma_ratio", 0.0)) * (float(s.std() or 0.0) or 1.0)
        return s + rng.normal(0.0, sigma, size=len(s))
    return s

def _classification_metrics(y_true, y_pred) -> dict:
    avg = "binary" if len(np.unique(y_true)) <= 2 else "weighted"
    try:
        return {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred, average=avg, zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, average=avg, zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, average=avg, zero_division=0)),
        }
    except Exception:
        return {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        }

def _regression_metrics(y_true, y_pred) -> dict:
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }

def _metric_card(label, baseline, perturbed, fmt=".4f",
                 higher_is_better=True, col_widths=None):
    col_widths = col_widths or {"xs": 12, "sm": 6, "md": 3}
    delta = perturbed - baseline
    good = (delta >= 0) if higher_is_better else (delta <= 0)
    color = "#198754" if good else "#DC3545"
    arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "→")
    return dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.Div(label, style={
                    "fontSize": "11px", "color": "#6C757D", "fontWeight": "600",
                    "textTransform": "uppercase", "letterSpacing": "0.5px",
                }),
                html.Div([
                    html.Span(f"{baseline:{fmt}}",
                              style={"color": "#6C757D", "fontSize": "13px"}),
                    html.Span(" → ", style={"color": "#ADB5BD", "margin": "0 6px"}),
                    html.Span(f"{perturbed:{fmt}}",
                              style={"fontWeight": "700", "fontSize": "18px"}),
                ], style={"marginTop": "4px"}),
                html.Div(
                    f"{arrow} {delta:+{fmt}}",
                    style={"color": color, "fontWeight": "700",
                           "fontSize": "12px", "marginTop": "2px"},
                ),
            ]),
            style={"borderLeft": f"4px solid {color}", "borderRadius": "8px"},
        ),
        **col_widths,
    )

def _info_card(label, value, color, col_widths=None):
    col_widths = col_widths or {"xs": 12, "sm": 6, "md": 3}
    return dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.Div(label, style={
                    "fontSize": "11px", "color": "#6C757D", "fontWeight": "600",
                    "textTransform": "uppercase", "letterSpacing": "0.5px",
                }),
                html.H4(value, style={"fontWeight": "700", "color": color, "marginBottom": 0}),
            ]),
            style={"borderLeft": f"4px solid {color}", "borderRadius": "8px"},
        ),
        **col_widths,
    )

def _figure_layout(title: str) -> dict:
    return dict(
        title=dict(text=title, font=dict(size=13, color="#212529"), x=0.01, xanchor="left"),
        height=320,
        margin=dict(l=40, r=20, t=46, b=36),
        legend=dict(orientation="h", y=1.10, x=1.0, xanchor="right", font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, system-ui, sans-serif", size=12, color="#495057"),
        xaxis=dict(
            showgrid=True, gridcolor="#F1F3F5", zeroline=False,
            linecolor="#DEE2E6", ticks="outside", tickcolor="#DEE2E6",
            tickfont=dict(size=11, color="#6C757D"),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#F1F3F5", zeroline=False,
            linecolor="#DEE2E6", ticks="outside", tickcolor="#DEE2E6",
            tickfont=dict(size=11, color="#6C757D"),
        ),
    )

class WhatIfCallbacks:
    def __init__(self, view: DataAnalyzerToolbox) -> None:
        self.view = view
        self.helper_func = HelperFunc()

    def register_callbacks(self):
        @self.view.app.callback(
            Output("wi-no-data-msg", "style"),
            Output("wi-content", "style"),
            Output("wi-feature-select", "options"),
            Output("wi-feature-select", "value"),
            Input("stored-model", "data"),
            Input("fe-stored-features", "data"),
        )
        def gate(model, features):
            if not model or not features:
                return VISIBLE, HIDDEN, [], None
            feature_cols = model.get("feature_cols") or features.get("feature_cols") or []
            X_test = pd.DataFrame(features.get("X_test", []))
            numeric_cols = [
                c for c in feature_cols
                if c in X_test.columns and pd.api.types.is_numeric_dtype(X_test[c])
            ]
            opts = [{"label": c, "value": c} for c in numeric_cols]
            default = numeric_cols[0] if numeric_cols else None
            return HIDDEN, VISIBLE, opts, default

        @self.view.app.callback(
            Output("wi-pert-param", "min"),
            Output("wi-pert-param", "max"),
            Output("wi-pert-param", "step"),
            Output("wi-pert-param", "value"),
            Output("wi-pert-param", "marks"),
            Output("wi-pert-param", "disabled"),
            Output("wi-pert-param-label", "children"),
            Output("wi-pert-param-wrap", "style"),
            Input("wi-pert-type", "value"),
            Input("wi-feature-select", "value"),
            State("fe-stored-features", "data"),
        )
        def configure_slider(pert_type, feature, features):
            if not features or not feature:
                return 0, 1, 0.01, 0, {}, True, "Pick a Feature First", {"display": "none"}

            X_test = pd.DataFrame(features["X_test"])
            if feature not in X_test.columns:
                return 0, 1, 0.01, 0, {}, True, "Feature not Found!", {"display": "none"},

            col = pd.to_numeric(X_test[feature], errors="coerce").dropna()
            if col.empty:
                return 0, 1, 0.01, 0, {}, True, "Feature Has no Numeric Values!", {"display": "none"},

            wrap_style = {"display": "block"}
            if pert_type == "scale":
                m = {0: "0×", 0.5: "0.5×", 1: "1×", 1.5: "1.5×", 2: "2×", 3: "3×"}
                return 0.0, 3.0, 0.05, 1.0, m, False, f"Multiplier for '{feature}'", wrap_style

            if pert_type == "noise":
                m = {0: "0", 0.25: "0.25×", 0.5: "0.5×", 1: "1×", 1.5: "1.5×", 2: "2×"}
                return 0.0, 2.0, 0.05, 0.5, m, False, f"Noise Level (× std) for '{feature}'", wrap_style

            return 0, 1, 0.01, 0, {}, True, "", {"display": "none"}

        @self.view.app.callback(
            Output("wi-metrics", "children"),
            Output("wi-viz", "children"),
            Input("wi-run-btn", "n_clicks"),
            Input("wi-reset-btn", "n_clicks"),
            State("wi-feature-select", "value"),
            State("wi-pert-type", "value"),
            State("wi-pert-param", "value"),
            State("wi-sample-frac", "value"),
            State("stored-model", "data"),
            State("fe-stored-features", "data"),
            prevent_initial_call=True,
        )
        def run_simulation(_run, _reset, feature, pert_type, param,
                           sample_frac, model, features):
            triggered = callback_context.triggered_id if hasattr(callback_context, "triggered_id") \
                else (callback_context.triggered[0]["prop_id"].split(".")[0]
                      if callback_context.triggered else None)

            if triggered == "wi-reset-btn":
                return "", ""

            if not model or not features or not feature:
                return dbc.Alert("Select a Feature and Run the Simulation.", color="info"), ""

            try:
                pipeline = pickle.loads(base64.b64decode(model["model_b64"]))
                task = model.get("task")
                feature_cols = model.get("feature_cols") or features.get("feature_cols")

                X_test = pd.DataFrame(features["X_test"])[feature_cols].reset_index(drop=True)
                y_raw = features.get("y_test")
                y_test = np.asarray(y_raw) if y_raw is not None and len(y_raw) > 0 else None

                n = len(X_test)
                if n == 0:
                    return dbc.Alert("Test Set is Empty!", color="warning"), ""

                params = {}
                if pert_type == "scale":
                    params["factor"] = float(1.0 if param is None else param)
                elif pert_type == "noise":
                    params["sigma_ratio"] = float(param or 0.0)

                frac = float(sample_frac or 100) / 100.0
                X_pert = X_test.copy()
                if frac >= 1.0:
                    X_pert[feature] = _apply_perturbation(
                        X_test[feature], pert_type, params, np.random.default_rng()
                    ).values
                    perturbed_count = n
                else:
                    k = max(1, int(round(n * frac)))
                    perturb_idx = np.random.default_rng().choice(n, size=k, replace=False)
                    perturbed_values = _apply_perturbation(
                        X_test[feature].iloc[perturb_idx], pert_type, params, np.random.default_rng()
                    )
                    X_pert.loc[perturb_idx, feature] = perturbed_values.values
                    perturbed_count = k

                X_base_safe = _safe_cols(X_test)
                X_pert_safe = _safe_cols(X_pert)
                y_base_pred = np.asarray(pipeline.predict(X_base_safe))
                y_pert_pred = np.asarray(pipeline.predict(X_pert_safe))

                if task == "classification":
                    flipped = int(np.sum(y_base_pred != y_pert_pred))
                    pct_flipped = (100.0 * flipped / n) if n else 0.0
                    w6 = {"xs": 12, "sm": 6, "md": 4, "lg": 2}

                    if y_test is not None:
                        base_m = _classification_metrics(y_test, y_base_pred)
                        pert_m = _classification_metrics(y_test, y_pert_pred)
                        metrics = dbc.Row([
                            _metric_card("Accuracy", base_m["accuracy"], pert_m["accuracy"], col_widths=w6),
                            _metric_card("Precision", base_m["precision"], pert_m["precision"], col_widths=w6),
                            _metric_card("Recall", base_m["recall"], pert_m["recall"], col_widths=w6),
                            _metric_card("F1 Score", base_m["f1"], pert_m["f1"], col_widths=w6),
                            _info_card("Rows Perturbed", f"{perturbed_count} / {n}", "#0DCAF0", col_widths=w6),
                            _info_card("Predictions Changed", f"{flipped} ({pct_flipped:.1f}%)", "#6F42C1", col_widths=w6),
                        ], className="g-3")
                    else:
                        metrics = html.Div([
                            dbc.Alert(
                                "No y_test In Features Store - Metrics Unavailable! "
                                "Showing Prediction Shift Only",
                                color="warning",
                            ),
                            dbc.Row([
                                _info_card("Rows Perturbed", f"{perturbed_count} / {n}", "#0DCAF0"),
                                _info_card("Predictions Changed", f"{flipped} ({pct_flipped:.1f}%)", "#6F42C1"),
                            ], className="g-3"),
                        ])

                elif task == "regression":
                    w4 = {"xs": 12, "sm": 6, "md": 3}
                    if y_test is not None:
                        base_m = _regression_metrics(y_test.astype(float), y_base_pred.astype(float))
                        pert_m = _regression_metrics(y_test.astype(float), y_pert_pred.astype(float))
                        metrics = dbc.Row([
                            _metric_card("MAE", base_m["mae"],  pert_m["mae"],  higher_is_better=False, col_widths=w4),
                            _metric_card("RMSE", base_m["rmse"], pert_m["rmse"], higher_is_better=False, col_widths=w4),
                            _metric_card("R²", base_m["r2"],   pert_m["r2"],   higher_is_better=True,  col_widths=w4),
                            _info_card("Rows perturbed", f"{perturbed_count} / {n}", "#0DCAF0", col_widths=w4),
                        ], className="g-3")
                    else:
                        metrics = html.Div([
                            dbc.Alert(
                                "No y_test in Features Store - Metrics Unavailable! "
                                "Showing Prediction Shift Only",
                                color="warning",
                            ),
                            dbc.Row([
                                _info_card("Rows perturbed", f"{perturbed_count} / {n}", "#0DCAF0"),
                            ], className="g-3"),
                        ])
                else:
                    metrics = dbc.Alert(f"Unknown Task Type: {task}", color="warning")

                fig_dist = go.Figure()
                fig_dist.add_trace(go.Histogram(
                    x=pd.to_numeric(X_test[feature], errors="coerce"),
                    name="Original",
                    marker=dict(color="#0D6EFD", line=dict(width=0)),
                    opacity=0.75,
                    nbinsx=40,
                ))
                fig_dist.add_trace(go.Histogram(
                    x=pd.to_numeric(X_pert[feature], errors="coerce"),
                    name="Perturbed",
                    marker=dict(color="#FD7E14", line=dict(width=0)),
                    opacity=0.75,
                    nbinsx=40,
                ))
                fig_dist.update_layout(
                    barmode="overlay",
                    **_figure_layout(f"Feature Distribution - {feature}"),
                )

                if task == "classification":
                    base_counts = pd.Series(y_base_pred).value_counts()
                    pert_counts = pd.Series(y_pert_pred).value_counts()
                    all_classes = sorted(set(base_counts.index) | set(pert_counts.index), key=lambda x: str(x))
                    fig_pred = go.Figure()
                    fig_pred.add_trace(go.Bar(
                        x=[str(c) for c in all_classes],
                        y=[int(base_counts.get(c, 0)) for c in all_classes],
                        name="Original",
                        marker=dict(color="#0D6EFD"),
                    ))
                    fig_pred.add_trace(go.Bar(
                        x=[str(c) for c in all_classes],
                        y=[int(pert_counts.get(c, 0)) for c in all_classes],
                        name="Perturbed",
                        marker=dict(color="#FD7E14"),
                    ))
                    fig_pred.update_layout(
                        barmode="group",
                        **_figure_layout("Predicted Classes"),
                    )
                else:
                    fig_pred = go.Figure()
                    fig_pred.add_trace(go.Scatter(
                        x=y_base_pred.astype(float),
                        y=y_pert_pred.astype(float),
                        mode="markers",
                        marker=dict(color="#FD7E14", size=7, opacity=0.7, line=dict(width=0)),
                        name="Perturbed",
                    ))
                    lo = float(min(np.min(y_base_pred), np.min(y_pert_pred)))
                    hi = float(max(np.max(y_base_pred), np.max(y_pert_pred)))
                    fig_pred.add_trace(go.Scatter(
                        x=[lo, hi], y=[lo, hi], mode="lines",
                        line=dict(color="#0D6EFD", dash="dash", width=2),
                        name="Original (y = x)",
                    ))
                    layout = _figure_layout("Predictions: original vs perturbed")
                    layout["xaxis"] = {**layout["xaxis"], "title": dict(text="Original", font=dict(size=11))}
                    layout["yaxis"] = {**layout["yaxis"], "title": dict(text="Perturbed", font=dict(size=11))}
                    fig_pred.update_layout(**layout)

                viz = dbc.Row([
                    dbc.Col(dcc.Graph(figure=fig_dist, config={"displayModeBar": False}), md=6),
                    dbc.Col(dcc.Graph(figure=fig_pred, config={"displayModeBar": False}), md=6),
                ], className="g-3")

                return metrics, viz

            except Exception as e:
                return dbc.Alert(f"Simulation Failed: {e}", color="danger"), ""
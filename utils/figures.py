import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.constants import CHART_LAYOUT
from utils.metrics import roc_curve_data

def empty_figure(title: str, message: str = "") -> go.Figure:
    fig = go.Figure()
    if message:
        fig.add_annotation(text=message, xref="paper", yref="paper",
                           x=0.5, y=0.5, showarrow=False,
                           font=dict(size=12, color="#6C757D"))
    fig.update_layout(title=title, xaxis=dict(visible=False),
                      yaxis=dict(visible=False), **CHART_LAYOUT)
    return fig

def roc_figure(y_true, y_proba) -> go.Figure:
    d = roc_curve_data(y_true, y_proba)
    fig = go.Figure()
    fig.add_scatter(x=d["fpr"], y=d["tpr"], mode="lines",
                    line=dict(color="#0D6EFD", width=2), name=f"ROC (AUC={d['auc']:.3f})")
    fig.add_scatter(x=[0, 1], y=[0, 1], mode="lines",
                    line=dict(color="#6C757D", dash="dash"), name="Chance")
    fig.update_layout(title=f"ROC Curve — AUC = {d['auc']:.3f}",
                      xaxis_title="False Positive Rate",
                      yaxis_title="True Positive Rate", **CHART_LAYOUT)
    return fig

def confusion_matrix_figure(y_true, y_pred) -> go.Figure:
    yt = pd.Series(y_true)
    yp = pd.Series(y_pred)
    classes = sorted(set(yt.unique()) | set(yp.unique()))
    labels = [str(c) for c in classes]
    idx = {c: i for i, c in enumerate(classes)}
    matrix = np.zeros((len(classes), len(classes)), dtype=int)
    for t, p in zip(yt, yp):
        matrix[idx[t]][idx[p]] += 1
    text = [[str(v) for v in row] for row in matrix]
    fig = go.Figure(data=go.Heatmap(
        z=matrix, x=labels, y=labels,
        text=text, texttemplate="%{text}",
        colorscale="Blues", showscale=False,
        hovertemplate="Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>",
    ))
    fig.update_layout(title="Confusion Matrix",
                      xaxis_title="Predicted", yaxis_title="Actual",
                      yaxis_autorange="reversed", **CHART_LAYOUT)
    return fig

def pred_vs_actual_figure(y_true, y_pred) -> go.Figure:
    yt = np.asarray(y_true, dtype=float)
    yp = np.asarray(y_pred, dtype=float)
    fig = go.Figure()
    fig.add_scatter(x=yt, y=yp, mode="markers",
                    marker=dict(size=5, color="#198754", opacity=0.6), name="Predictions")
    lo, hi = float(min(yt.min(), yp.min())), float(max(yt.max(), yp.max()))
    fig.add_scatter(x=[lo, hi], y=[lo, hi], mode="lines",
                    line=dict(color="#DC3545", dash="dash"), name="y = x")
    fig.update_layout(title="Predicted vs. Actual",
                      xaxis_title="Actual", yaxis_title="Predicted", **CHART_LAYOUT)
    return fig

def residuals_figure(y_true, y_pred) -> go.Figure:
    residuals = np.asarray(y_true, dtype=float) - np.asarray(y_pred, dtype=float)
    fig = go.Figure(data=go.Histogram(x=residuals, marker_color="#0D6EFD", nbinsx=40))
    fig.update_layout(title="Residual Distribution (y_true − y_pred)",
                      xaxis_title="Residual", yaxis_title="Count", **CHART_LAYOUT)
    return fig

def diagnostics(task, y_test, y_pred, y_proba):
    if task == "classification":
        if y_proba is not None and y_proba.ndim == 2 and y_proba.shape[1] == 2:
            d1 = roc_figure(y_test, y_proba)
        else:
            msg = "Probability scores not available (multiclass or estimator without predict_proba)."
            d1 = empty_figure("ROC Curve", msg)
        return d1, confusion_matrix_figure(y_test, y_pred)
    return (
        pred_vs_actual_figure(y_test, y_pred),
        residuals_figure(y_test, y_pred),
    )
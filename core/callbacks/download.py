import pandas as pd
import datetime as dt
import io, json, base64, zipfile
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, no_update
from core.view.data_analyzer_toolbox import DataAnalyzerToolbox
from utils.dataframe import HIDDEN, VISIBLE

def _fmt_metric(v) -> str:
    if isinstance(v, dict):
        val = v.get("value")
        if val is None:
            return "—"
        return f"{val:.4f}"
    if isinstance(v, (int, float)):
        return f"{v:.4f}"
    return str(v)

def _build_model_card(model: dict, metrics: dict, dataset_rows: int | None) -> str:
    family = model.get("family", "—")
    algorithm = model.get("algorithm", "—")
    task = model.get("task", "—")
    params = model.get("params") or {}
    feature_cols = model.get("feature_cols") or []
    target_col = model.get("target_col", "—")

    metric_block = "_No Metrics Available._"
    if metrics:
        m = metrics.get("metrics") or {}
        if m:
            rows = [f"| {k} | {_fmt_metric(v)} |" for k, v in m.items()]
            metric_block = (
                "| Metric | Value (95% CI) |\n"
                "|---|---|\n" + "\n".join(rows)
            )

    param_block = "_None_"
    if params:
        param_block = "\n".join(f"- `{k}`: `{v}`" for k, v in params.items())

    feature_block = ", ".join(f"`{c}`" for c in feature_cols) or "_None_"

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
        # Model Card

        _Generated: {now}_

        ## Overview

        - **Task:** {task}
        - **Family:** {family}
        - **Algorithm:** {algorithm}
        - **Target column:** `{target_col}`
        - **Training rows (post-clean):** {dataset_rows if dataset_rows is not None else "—"}

        ## Hyperparameters

        {param_block}

        ## Features

        {feature_block}

        ## Test-set Metrics

        {metric_block}

        ## Reproducibility

        - Random seed: `42` (project-wide)
        - Preprocessing + estimator wrapped in `sklearn.pipeline.Pipeline`
        - Test split frozen in `stored-split` and never modified
        """

def _metrics_json(model: dict, metrics: dict) -> str:
    payload = {
        "family": model.get("family"),
        "algorithm": model.get("algorithm"),
        "task": model.get("task"),
        "params": model.get("params") or {},
        "feature_cols": model.get("feature_cols") or [],
        "target_col": model.get("target_col"),
        "metrics": (metrics or {}).get("metrics") or {},
    }
    return json.dumps(payload, indent=2, default=str)

def _dataset_csv(dataset_records) -> str:
    df = pd.DataFrame(dataset_records or [])
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue()

def _model_bytes(model: dict) -> bytes:
    b64 = (model or {}).get("model_b64")
    if not b64:
        return b""
    return base64.b64decode(b64)

def _summary_view(model: dict, metrics: dict, dataset_records) -> html.Div:
    if not model:
        return dbc.Alert(
            "Train a Model to Enable Downloads.",
            color="info",
        )

    pills = []
    task = str(model.get("task", "—")).upper()
    family = str(model.get("family", "—")).upper()
    algorithm = str(model.get("algorithm", "—")).upper()
    for label, value in [
        ("Task", task),
        ("Family", family),
        ("Algorithm", algorithm),
        ("Features", len(model.get("feature_cols") or [])),
        ("Rows", len(dataset_records or [])),
    ]:
        pills.append(
            html.Div(
                [
                    html.Div(
                        label,
                        style={
                            "fontSize": "11px",
                            "color": "#6C757D",
                            "fontWeight": "600",
                            "textTransform": "uppercase",
                            "letterSpacing": "0.5px",
                        },
                    ),
                    html.Div(
                        str(value),
                        style={"fontWeight": "700", "fontSize": "16px",
                               "color": "#212529", "marginTop": "2px"},
                    ),
                ],
                style={
                    "padding": "10px 14px",
                    "border": "1px solid #E9ECEF",
                    "borderRadius": "8px",
                    "backgroundColor": "#F8F9FA",
                    "minWidth": "140px",
                },
            )
        )

    m = (metrics or {}).get("metrics") or {}
    metric_rows = [
        html.Tr([
            html.Td(
                k,
                style={"fontWeight": "600", "fontSize": "13px",
                       "padding": "8px 12px"},
            ),
            html.Td(
                _fmt_metric(v),
                style={"fontSize": "13px", "fontFamily": "monospace",
                       "padding": "8px 12px", "textAlign": "right",
                       "color": "#212529"},
            ),
        ])
        for k, v in m.items()
    ]

    if metric_rows:
        metric_block = html.Div(
            dbc.Table(
                [
                    html.Thead(html.Tr([
                        html.Th(
                            "Metric",
                            style={"textAlign": "left", "padding": "8px 12px",
                                   "fontSize": "12px",
                                   "textTransform": "uppercase",
                                   "letterSpacing": "0.5px",
                                   "color": "#6C757D",
                                   "backgroundColor": "#F8F9FA"},
                        ),
                        html.Th(
                            "Value",
                            style={"textAlign": "right", "padding": "8px 12px",
                                   "fontSize": "12px",
                                   "textTransform": "uppercase",
                                   "letterSpacing": "0.5px",
                                   "color": "#6C757D",
                                   "backgroundColor": "#F8F9FA"},
                        ),
                    ])),
                    html.Tbody(metric_rows),
                ],
                bordered=False,
                hover=True,
                striped=True,
                size="sm",
                style={"marginBottom": "0",
                       "border": "1px solid #E9ECEF",
                       "borderRadius": "8px",
                       "overflow": "hidden"},
            ),
            style={"marginTop": "16px"},
        )
    else:
        metric_block = html.Div(
            "No Metrics Recorded Yet!",
            style={"fontSize": "12px", "color": "#6C757D", "marginTop": "8px"},
        )

    return html.Div([
        html.Div(pills, style={"display": "flex", "flexWrap": "wrap", "gap": "12px"}),
        metric_block,
    ])

class DownloadCallbacks:
    def __init__(self, view: DataAnalyzerToolbox) -> None:
        self.view = view

    def register_callbacks(self):
        @self.view.app.callback(
            Output("dl-no-data-msg", "style"),
            Output("dl-content", "style"),
            Output("dl-summary", "children"),
            Input("stored-model", "data"),
            Input("stored-metrics", "data"),
            Input("stored-dataset", "data"),
        )
        def gate(model, metrics, dataset):
            if not model:
                return VISIBLE, HIDDEN, no_update
            return HIDDEN, VISIBLE, _summary_view(model, metrics, dataset)

        @self.view.app.callback(
            Output("dl-model-file", "data"),
            Input("dl-model-btn", "n_clicks"),
            State("stored-model", "data"),
            prevent_initial_call=True,
        )
        def download_model(_n, model):
            data = _model_bytes(model)
            if not data:
                return no_update
            return dcc.send_bytes(data, filename="model.pkl")

        @self.view.app.callback(
            Output("dl-card-file", "data"),
            Input("dl-card-btn", "n_clicks"),
            State("stored-model", "data"),
            State("stored-metrics", "data"),
            State("stored-dataset", "data"),
            prevent_initial_call=True,
        )
        def download_card(_n, model, metrics, dataset):
            if not model:
                return no_update
            n_rows = len(dataset) if dataset else None
            md = _build_model_card(model, metrics or {}, n_rows)
            return dcc.send_string(md, filename="model_card.md")

        @self.view.app.callback(
            Output("dl-data-file", "data"),
            Input("dl-data-btn", "n_clicks"),
            State("stored-dataset", "data"),
            prevent_initial_call=True,
        )
        def download_data(_n, dataset):
            if not dataset:
                return no_update
            return dcc.send_string(_dataset_csv(dataset), filename="dataset.csv")

        @self.view.app.callback(
            Output("dl-bundle-file", "data"),
            Input("dl-bundle-btn", "n_clicks"),
            State("stored-model", "data"),
            State("stored-metrics", "data"),
            State("stored-dataset", "data"),
            prevent_initial_call=True,
        )
        def download_bundle(_n, model, metrics, dataset):
            if not model:
                return no_update

            buf = io.BytesIO()
            n_rows = len(dataset) if dataset else None
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                model_bytes = _model_bytes(model)
                if model_bytes:
                    zf.writestr("model.pkl", model_bytes)
                zf.writestr(
                    "model_card.md",
                    _build_model_card(model, metrics or {}, n_rows),
                )
                zf.writestr(
                    "metrics.json",
                    _metrics_json(model, metrics or {}),
                )
                if dataset:
                    zf.writestr("dataset.csv", _dataset_csv(dataset))

            return dcc.send_bytes(buf.getvalue(), filename="artifacts.zip")

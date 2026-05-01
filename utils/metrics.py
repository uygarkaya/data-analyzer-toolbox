import numpy as np
from typing import Dict, Tuple
from sklearn.metrics import (
    f1_score, roc_curve,
    accuracy_score,
    mean_squared_error,
    mean_absolute_error,
    median_absolute_error,
    r2_score, auc,
)

def _ci(values: np.ndarray) -> Tuple[float, float]:
    lo = float(np.percentile(values, 2.5))
    hi = float(np.percentile(values, 97.5))
    return lo, hi

def _classification_point(y_true, y_pred, y_proba=None) -> Dict[str, float]:
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
    }

def _regression_point(y_true, y_pred) -> Dict[str, float]:
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "med_ae": float(median_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }

def compute_with_ci(task: str, y_true, y_pred, y_proba=None, n_boot: int = 30, seed: int = 42) -> Dict[str, Dict[str, float]]:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    y_proba = np.asarray(y_proba) if y_proba is not None else None

    if task == "classification":
        point = _classification_point(y_true, y_pred, y_proba)
    else:
        point = _regression_point(y_true, y_pred)

    rng = np.random.default_rng(seed)
    n = len(y_true)
    boots: Dict[str, list] = {k: [] for k in point}

    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        yt = y_true[idx]
        yp = y_pred[idx]
        ypr = y_proba[idx] if y_proba is not None else None
        try:
            sample = (_classification_point(yt, yp, ypr) if task == "classification" else _regression_point(yt, yp))
        except Exception:
            continue
        for k, v in sample.items():
            if k in boots:
                boots[k].append(v)

    out: Dict[str, Dict[str, float]] = {}
    for k, v in point.items():
        if boots[k]:
            lo, hi = _ci(np.asarray(boots[k]))
        else:
            lo = hi = float("nan")
        out[k] = {"value": v, "ci_low": lo, "ci_high": hi}
    return out

def roc_curve_data(y_true, y_proba) -> Dict[str, np.ndarray]:
    y_true = np.asarray(y_true)
    scores = y_proba[:, 1]
    fpr, tpr, _ = roc_curve(y_true, scores)
    return {"fpr": fpr, "tpr": tpr, "auc": float(auc(fpr, tpr))}

import pandas as pd

HIDDEN = {"display": "none"}
VISIBLE = {"display": "block"}

def dropdown_options(columns):
    return [{"label": c, "value": c} for c in columns]

def table_columns(df):
    return [{"name": c, "id": c} for c in df.columns]

def shape_label(df):
    return f"{len(df):,} Rows × {len(df.columns)} Columns"

def preview_data(df, n=20):
    return df.head(n).to_dict("records")

def detect_task_type(series):
    n_unique = series.nunique()
    if series.dtype == "object" or n_unique == 2:
        task_type = "Binary Classification" if n_unique == 2 else "Multiclass Classification"
        color = "primary" if n_unique == 2 else "info"
    elif pd.api.types.is_integer_dtype(series) and 2 < n_unique <= 20:
        task_type = "Multiclass Classification"
        color = "info"
    else:
        task_type = "Regression"
        color = "warning"
    return task_type, color

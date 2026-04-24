LIGHT = {
    "bg":       "#f5f5f0",
    "surface":  "#ffffff",
    "surface2": "#eeeee8",
    "border":   "#d8d8d0",
    "text":     "#1a1a2e",
    "sub":      "#6b7280",
    "hint":     "#9ca3af",
}

TAB_ACCENT = {
    0: {"color": "#1a7a4a", "bg": "#e8f5ee"},
    1: {"color": "#1d5fa8", "bg": "#e8f0fb"},
    2: {"color": "#6d3fa8", "bg": "#f0ebfb"},
    3: {"color": "#b85c1a", "bg": "#fdf0e8"},
    4: {"color": "#9a6c10", "bg": "#fdf5e0"},
    5: {"color": "#1a7a4a", "bg": "#e8f5ee"},
    6: {"color": "#1d5fa8", "bg": "#e8f0fb"},
    7: {"color": "#6d3fa8", "bg": "#f0ebfb"},
    8: {"color": "#b85c1a", "bg": "#fdf0e8"},
}

TABLE_STYLE = {
    "table": {
        "overflowX": "auto",
        "borderRadius": "8px",
        "border": "1px solid #DEE2E6",
    },
    "header": {
        "backgroundColor": "#F8F9FA",
        "fontWeight": "700",
        "fontSize": "12px",
        "textTransform": "uppercase",
        "letterSpacing": "0.4px",
        "color": "#495057",
        "borderBottom": "2px solid #DEE2E6",
    },
    "cell": {
        "fontSize": "13px",
        "fontFamily": "sans-serif",
        "textAlign": "left",
        "whiteSpace": "normal",
        "maxWidth": "200px",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
    },
    "striped": [
        {"if": {"row_index": "odd"}, "backgroundColor": "#F8F9FA"},
    ],
}

CHART_LAYOUT = {
    "margin": dict(l=20, r=20, t=20, b=20),
    "template": "plotly_white",
    "font": dict(family="sans-serif"),
}

TYPE_STYLES = {
    "classification": {
        "color": "primary"
    },
    "regression": {
        "color": "success"
    },
}
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

SECTION_TITLE_STYLE = {
    "fontWeight": "700",
    "marginBottom": "4px",
}

SECTION_SUBTITLE_STYLE = {
    "color": "#6C757D",
    "marginBottom": "24px",
    "fontWeight": "400",
}

LABEL_STYLE = {
    "fontWeight": "600",
    "fontSize": "13px",
}

CARD_STYLE = {
    "borderRadius": "10px",
    "boxShadow": "0 1px 6px rgba(0,0,0,0.07)",
}

SECTION_DIVIDER_STYLE = {
    "margin": "32px 0 24px 0",
    "border": "none",
    "borderTop": "1px solid #DEE2E6",
}

_INNER_TAB_BASE = {
    "padding": "6px 12px",
    "fontSize": "0.80rem",
    "fontWeight": "700",
    "letterSpacing": "0.05em",
    "textTransform": "uppercase",
    "border": "none",
    "backgroundColor": "transparent",
}

INNER_TAB_STYLE = {**_INNER_TAB_BASE}
INNER_TAB_SELECTED_STYLE = {
    **_INNER_TAB_BASE,
    "borderBottom": "2px solid #0D6EFD",
    "color": "#0D6EFD",
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
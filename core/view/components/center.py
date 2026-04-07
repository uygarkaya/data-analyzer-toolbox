import dash_bootstrap_components as dbc
from dash import html
from configuration.configuration import Configuration
from utils.constants import LIGHT, TAB_ACCENT

class Center:
    def __init__(self) -> None:
        self.config = Configuration()
    
    def get_tab_content(self, tab_id, tab_label):
        component = self.config.tabs_components.get(tab_id)

        if component:
            return component().content()

        return html.Div(f"{tab_label} Content")

    def build_tab(self, tab_id: str, tab_label: str, index: int) -> dbc.Tab:
        accent = TAB_ACCENT.get(index, {"color": LIGHT["sub"], "bg": LIGHT["surface2"]})
        color = accent["color"]

        return dbc.Tab(
            tab_id=tab_id,
            label=tab_label,
            label_style={
                "fontFamily": "sans-serif",
                "fontWeight": "700",
                "fontSize": "0.80rem",
                "letterSpacing": "0.05em",
                "textTransform": "uppercase",
                "color": LIGHT["hint"],
            },
            active_label_style={
                "color": color,
                "backgroundColor": LIGHT["surface"],
                "borderColor": LIGHT["border"],
                "borderBottomColor": LIGHT["surface"],
            },
            children=[
                html.Div(
                    [
                        self.get_tab_content(tab_id, tab_label)                            
                    ],
                    style={
                        "display": "flex",
                        "flex": 1,
                        "minHeight": 0,
                        "flexDirection": "column",
                        "alignItems": "stretch",
                        "padding": "20px 22px",
                        "backgroundColor": LIGHT["surface"],
                        "border": f"1px solid {LIGHT['border']}",
                        "width": "100%",
                        "overflowY": "auto", 
                    },
                )
            ],
        )

    def center(self) -> html.Div:
        tabs = [
            self.build_tab(tab_id, tab_label, i)
            for i, (tab_id, tab_label) in enumerate(self.config.tabs.items())
        ]

        return html.Div(
            [
                html.Div(
                    dbc.Tabs(
                        tabs,
                        id="main-tabs",
                        active_tab=list(self.config.tabs.keys())[0],
                        style={
                            "backgroundColor": LIGHT["surface2"],
                            "borderRadius": "8px 8px 0 0",
                            "borderBottom": f"1px solid {LIGHT['border']}",
                        },
                    ),
                    style={
                        "backgroundColor": LIGHT["bg"],
                        "borderRadius": "14px",
                        "border": f"1px solid {LIGHT['border']}",
                        "overflow": "auto",
                        "display": "flex",
                        "flexDirection": "column",
                        "flex": 1,
                        "minHeight": 0,
                    },
                )
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "width": "100%",
                "height": "100%",
                "flex": 1,
                "paddingLeft": "1rem",
                "paddingRight": "1rem",
                "fontFamily": "sans-serif",
            },
        )
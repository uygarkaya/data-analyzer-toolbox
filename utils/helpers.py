from dash import html
import dash_bootstrap_components as dbc

class HelperFunc:
    def __init__(self) -> None:
        pass

    def data_overview_stat_card(self, card_id: str, label: str, color: str) -> dbc.Col:
        return dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.Span(label, style={"fontSize": "12px", "color": "#6c757d", "fontWeight": "600", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
                    ], style={"display": "flex", "alignItems": "center", "marginBottom": "6px"}),
                    html.H4(
                        id=card_id,
                        children="—",
                        style={"fontWeight": "700", "color": color, "marginBottom": "0"}
                    )
                ]),
                style={"borderLeft": f"4px solid {color}", "borderRadius": "8px", "boxShadow": "0 1px 6px rgba(0,0,0,0.07)"}
            ),
            xs=12, sm=6, md=3, style={"marginBottom": "16px"}
        )
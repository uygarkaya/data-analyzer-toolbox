from dash import html, dcc
import dash_bootstrap_components as dbc

class HelperFunc:
    def __init__(self) -> None:
        pass

    def data_overview_stat_card(self, card_id: str, label: str, color: str) -> dbc.Col:
        return dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.Span(label, style={"fontSize": "12px", "color": "#6C757D", "fontWeight": "600", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
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
    
    def eda_chart_card(self, title: str, graph_id: str) -> dbc.Card:
        return dbc.Card(
            dbc.CardBody([
                html.H6(title, style={"fontWeight": "600", "marginBottom": "12px", "color": "#343A40"}),
                dcc.Loading(
                    dcc.Graph(
                        id=graph_id,
                        config={"displayModeBar": False},
                        style={"height": "320px"}
                    ),
                    type="circle",
                    color="#0D6EFD"
                )
            ]),
            style={"borderRadius": "10px", "boxShadow": "0 1px 6px rgba(0,0,0,0.07)", "marginBottom": "20px"}
        )

    def data_processing_section_card(self, title: str, body: list) -> dbc.Card:
        return dbc.Card(
            [
                dbc.CardHeader(
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span(title, style={"fontWeight": "700", "fontSize": "14px", "display": "block"}),
                                ]
                            ),
                        ],
                        style={"display": "flex", "alignItems": "center"},
                    )
                ),
                dbc.CardBody(body),
            ],
            style={
                "borderRadius": "10px",
                "boxShadow": "0 1px 6px rgba(0,0,0,0.07)",
                "height": "100%",
            },
        )
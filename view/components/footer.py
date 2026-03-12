from dash import html

class Footer:
    def __init__(self) -> None:
        pass

    def footer(self) -> html.Div:
        return html.Div(
            [html.Span("Copyright © 2026 Uygar Kaya - Practical Application of Data Science Course")],
            id="footer-general",
            className="footer-general",
            style={
                "justifyContent": "center",
                "alignItems": "center",
                "color": "#FFFFFF",
                "position": "fixed",
                "bottom": "0",
                "width": "100%",
                "height": "40px",
                "display": "flex",
                "fontFamily": "sans-serif",
                "backgroundImage": "linear-gradient(to right, #0e9d59, #00898d)",
            }
        )
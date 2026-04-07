import dash_bootstrap_components as dbc

class Notification:
    def __init__(self):
        self.alert_id = "popup-notification"

    def generate_alert(self, message, color="success", duration=4000) -> dbc.Alert:
        print(f"Generating alert: {message} (color={color}, duration={duration}ms)")
        return dbc.Alert(
            id=self.alert_id,
            children=message,
            color=color,
            dismissable=True,
            duration=duration,
            style={
                "position": "fixed",
                "right": "20px",
                "zIndex": 9999,
                "minWidth": "250px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.15)",
                "borderRadius": "5px",
            }
        )
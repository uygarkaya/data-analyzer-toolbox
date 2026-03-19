from dash import callback, Output, Input
import pandas as pd
import base64, io
import dash_bootstrap_components as dbc

from core.view.dataset_analyzer_toolbox import DatasetAnalyzerToolbox

class CoreCallbacks:
    def __init__(self, view: DatasetAnalyzerToolbox) -> None:
        self.view = view

    def register_callbacks(self):
        @callback(
            Output("stored-dataset", "data"),
            Output("upload-alert-container", "children"),
            Input("upload-dataset", "contents"),
            prevent_initial_call=True
        )
        def store_uploaded_dataset(contents):
            if contents is None:
                return None, None

            content_type, content_string = contents.split(",")
            if "csv" not in content_type:
                alert = self.view.generate_alert(
                    "Unsupported File Format! Please Upload a CSV File",
                    color="danger"
                )
                return None, alert

            try:
                decoded = base64.b64decode(content_string)
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

                alert = self.view.generate_alert(
                    "Dataset Uploaded Successfully!",
                    color="success"
                )
                

                return df.to_dict("records"), alert

            except Exception as e:
                alert = self.view.generate_alert(
                    f"Error Reading File: {str(e)}",
                    color="danger"
                )
                return None, alert
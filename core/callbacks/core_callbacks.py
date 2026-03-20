from dash import callback, Output, Input
from dash import ctx, ALL
import pandas as pd
import base64, io
import dash_bootstrap_components as dbc

from core.api.dataset import DatasetAPI
from core.view.dataset_analyzer_toolbox import DatasetAnalyzerToolbox

class CoreCallbacks:
    def __init__(self, view: DatasetAnalyzerToolbox) -> None:
        self.view = view

    def register_callbacks(self):
        @callback(
            Output("stored-dataset", "data", allow_duplicate=True),
            Output("upload-alert-container", "children", allow_duplicate=True),
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
            
        @callback(
            Output("stored-dataset", "data", allow_duplicate=True),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input({"type": "sample-dataset-btn", "index": ALL}, "n_clicks"),
            prevent_initial_call=True
        )
        def load_sample_dataset(n_clicks_list):
            if not any(n_clicks_list):
                return None, None

            triggered_id = ctx.triggered_id
            dataset_id = triggered_id["index"]

            df, entry, error = DatasetAPI.download_dataset(dataset_id)

            if error:
                return None, dbc.Alert(f"Error: {error}", color="danger")

            return df.to_dict("records"), dbc.Alert(
                f"{entry['name']} Loaded Successfully!",
                color="success"
            )
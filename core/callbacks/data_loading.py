from dash import Output, Input, ALL
from dash import ctx
import pandas as pd
import base64, io, requests

from core.api.dataset import DatasetAPI
from core.view.dataset_analyzer_toolbox import DatasetAnalyzerToolbox
from utils.helpers import HelperFunc

class DataLoadingCallbacks:
    def __init__(self, view: DatasetAnalyzerToolbox) -> None:
        self.view = view
        self.helper_func_func = HelperFunc()

    def register_callbacks(self):
        @self.view.app.callback(
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
                alert = self.helper_func_func.generate_alert(
                    "Unsupported File Format! Please Upload a CSV File",
                    color="danger"
                )
                return None, alert

            try:
                decoded = base64.b64decode(content_string)
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

                alert = self.helper_func_func.generate_alert(
                    "Dataset Uploaded Successfully!",
                    color="success"
                )

                return df.to_dict("records"), alert

            except Exception as e:
                alert = self.helper_func_func.generate_alert(
                    f"Error Reading File: {str(e)}",
                    color="danger"
                )
                return None, alert

        @self.view.app.callback(
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
                return None, self.helper_func_func.generate_alert(f"Error: {error}", color="danger")

            return df.to_dict("records"), self.helper_func_func.generate_alert(
                f"{entry['name']} Loaded Successfully!",
                color="success"
            )

        @self.view.app.callback(
            Output("stored-dataset", "data", allow_duplicate=True),
            Output("upload-alert-container", "children", allow_duplicate=True),
            Input("fetch-api-btn", "n_clicks"),
            Input("api-url", "value"),
            prevent_initial_call=True
        )
        def fetch_dataset_from_api(n_clicks, url):
            if not n_clicks or not url:
                return None, None

            try:
                response = requests.get(url)

                if response.status_code != 200:
                    alert = self.helper_func_func.generate_alert(
                        f"Failed to Fetch Data! Status Code: {response.status_code}",
                        color="danger"
                    )
                    return None, alert

                df = pd.read_csv(io.StringIO(response.text))
                alert = self.helper_func_func.generate_alert(
                    "Dataset Fetched Successfully from API!",
                    color="success"
                )

                return df.to_dict("records"), alert

            except Exception as e:
                alert = self.helper_func_func.generate_alert(
                    f"Error Fetching API Data: {str(e)}",
                    color="danger"
                )
                return None, alert

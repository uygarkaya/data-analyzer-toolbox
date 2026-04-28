import dash_bootstrap_components as dbc
import pandas as pd
import io, requests

from dash import Output, Input
from dash import ctx, html, ALL
from utils.helpers import HelperFunc
from core.api.dataset import DatasetAPI
from configuration.configuration import Configuration
from core.view.data_analyzer_toolbox import DataAnalyzerToolbox

class DataLoadingCallbacks:
    def __init__(self, view: DataAnalyzerToolbox) -> None:
        self.view = view
        self.helper_func_func = HelperFunc()

    def register_callbacks(self):
        @self.view.app.callback(
            Output("fetch-data-tab-content", "children"),
            Input("fetch-data-tabs", "value"),
        )
        def render_fetch_data_tab(value):
            if value == "fetch-data-sample":
                return html.Div(
                    dbc.Row(
                        [HelperFunc.sample_dataset_card(d) for d in Configuration().sample_datasets],
                        className="g-3",
                    ),
                    style={"padding": "4px"},
                )
            return dbc.Row(
                [
                    dbc.Col(
                        dbc.Input(
                            id="api-url",
                            placeholder="https://api.example.com/dataset",
                            type="text",
                        ),
                        width=9,
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Fetch Data",
                            id="fetch-api-btn",
                            color="primary",
                            className="w-100",
                        ),
                        width=3,
                    ),
                ]
            )

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

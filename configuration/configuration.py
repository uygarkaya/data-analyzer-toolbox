from core.view.components.tabs.fetch_data import FetchData
from core.view.components.tabs.data_overview import DataOverview
from core.view.components.tabs.data_processing import DataProcessing
from core.view.components.tabs.feature_engineering import FeatureEngineering
from core.view.components.tabs.exploratory_data_analysis import ExploratoryDataAnalysis
from configuration.environment import Environment
from typing import Dict

from utils.helpers import HelperFunc

class Configuration:
    def __init__(self):
        self.environment: Environment = Environment.get_instance()
        self.system_host: str = self.environment['HOST']
        self.system_port: str = self.environment['PORT']
        self.dataset_url: str = self.environment['DATASET_URL']
        self.tabs: Dict[str, str] = {
            "tab-fetch": "Fetch Datasets",
            "tab-info": "Dataset Information",
            "tab-eda": "Exploratory Data Analysis",
            "tab-process": "Data Processing",
            "tab-feature": "Feature Engineering",
            "tab-train": "Train Model",
            "tab-evaluate": "Evaluate",
            "tab-explainability": "Explainability",
            "tab-download": "Download Dataset",
        }

        self.tabs_components: Dict[str, type] = {
            "tab-fetch": FetchData,
            "tab-info": DataOverview,
            "tab-eda": ExploratoryDataAnalysis,
            "tab-process": DataProcessing,
            "tab-feature": FeatureEngineering,
        }

        self.helper_func: HelperFunc = HelperFunc()
        self.sample_datasets: list = self.helper_func.load_json(self.dataset_url)
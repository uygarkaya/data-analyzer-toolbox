from core.view.components.tabs.fetch_data import FetchData
from core.view.components.tabs.data_overview import DataOverview
from core.view.components.tabs.data_processing import DataProcessing
from core.view.components.tabs.feature_engineering import FeatureEngineering
from core.view.components.tabs.exploratory_data_analysis import ExploratoryDataAnalysis
from core.view.components.tabs.train_model import TrainModel
from configuration.environment import Environment
from utils.models_catalog import ModelsCatalog
from utils.helpers import HelperFunc
from typing import Dict

class Configuration:
    def __init__(self):
        self.environment: Environment = Environment.get_instance()
        self.system_host: str = self.environment['HOST']
        self.system_port: str = self.environment['PORT']
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
            "tab-train": TrainModel,
        }

        self.sample_datasets: list = HelperFunc().load_json(self.environment['DATASET_URL'])
        self.models_catalog: ModelsCatalog = ModelsCatalog(self.environment['MODELS_URL'])
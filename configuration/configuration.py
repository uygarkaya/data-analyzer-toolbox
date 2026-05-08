from core.view.components.tabs.data_explorer import DataExplorer
from core.view.components.tabs.data_processing import DataProcessing
from core.view.components.tabs.feature_engineering import FeatureEngineering
from core.view.components.tabs.train_evaluate import TrainEvaluate
from core.view.components.tabs.explainability import Explainability
from configuration.environment import Environment
from utils.helpers import HelperFunc
from typing import Dict

class Configuration:
    def __init__(self):
        self.environment: Environment = Environment.get_instance()
        self.system_host: str = self.environment['HOST']
        self.system_port: str = self.environment['PORT']
        self.tabs: Dict[str, str] = {
            "tab-explore": "Data Explorer",
            "tab-process": "Data Processing",
            "tab-feature": "Feature Engineering",
            "tab-train": "Train-Evaluate Model",
            "tab-explainability": "Explainability",
            "tab-what-if": "What-If Simulation",
            "tab-download": "Download",
        }

        self.tabs_components: Dict[str, type] = {
            "tab-explore": DataExplorer,
            "tab-process": DataProcessing,
            "tab-feature": FeatureEngineering,
            "tab-train": TrainEvaluate,
            "tab-explainability": Explainability,
        }

        self.sample_datasets: list = HelperFunc().load_json(self.environment['DATASET_URL'])
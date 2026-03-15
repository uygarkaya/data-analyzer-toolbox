from core.view.components.tabs.fetch_data import FetchData
from configuration.environment import Environment
from typing import Dict

class Configuration:
    def __init__(self):
        self.environment: Environment = Environment.get_instance()
        self.system_host: str = self.environment['HOST']
        self.system_port: str = self.environment['PORT']
        self.tabs: Dict[str, str] = {
            "tab-fetch": "Fetch Datasets",
            "tab-eda": "Exploratory Data Analysis",
            "tab-clean": "Clean Data",
            "tab-train": "Train Model",
            "tab-evaluate": "Evaluate",
        }

        self.tabs_components = {
            "tab-fetch": FetchData
        }
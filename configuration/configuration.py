from core.view.components.tabs.fetch_data import FetchData
from core.view.components.tabs.data_overview import DataOverview
from core.view.components.tabs.exploratory_data_analysis import ExploratoryDataAnalysis
from configuration.environment import Environment
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
            "tab-clean": "Clean Data",
            "tab-train": "Train Model",
            "tab-evaluate": "Evaluate",
        }

        self.tabs_components = {
            "tab-fetch": FetchData,
            "tab-info": DataOverview,
            "tab-eda": ExploratoryDataAnalysis,
        }

        self.sample_datasets = [
            {
                "id": "iris-dataset",
                "name": "01 - Iris Flowers Dataset - [Multiclass Classification]",
                "type": "classification",
                "format": "csv",
                "description": "Classic Multiclass Classification Dataset (150 rows x 5 cols)",
                "url": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv",
                "target_col": "species",
            },
            {
                "id": "titanic-dataset",
                "name": "02 - Titanic Passengers Dataset - [Binary Survival Classification]",
                "type": "classification",
                "format": "csv",
                "description": "Binary Survival Classification (891 rows x 12 cols)",
                "url": "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
                "target_col": "Survived",
            },
            {
                "id": "california-housing-dataset",
                "name": "03 - California Housing Dataset - [Regression]",
                "type": "regression",
                "format": "csv",
                "description": "Median House Price Regression",
                "url": "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv",
                "target_col": "median_house_value",
            },
            {
                "id": "wine-dataset",
                "name": "04 - Wine Quality Dataset - [Regression]",
                "type": "regression",
                "format": "csv",
                "description": "Wine quality score regression (1599 rows x 12 cols)",
                "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
                "target_col": "quality",
            },
        ]
from core.view.data_analyzer_toolbox import DataAnalyzerToolbox
from core.callbacks.data_fetch import DataLoadingCallbacks
from core.callbacks.data_overview import DataOverviewCallbacks
from core.callbacks.exp_data_analysis import EdaCallbacks
from core.callbacks.data_processing import DataProcessingCallbacks
from core.callbacks.feature_engineering import FeatureEngineeringCallbacks
from core.callbacks.train_evaluate import TrainEvaluateCallbacks
from core.callbacks.explainability import ExplainabilityCallbacks
from configuration.configuration import Configuration

class DatasetAnalyzerApplication:
    def __init__(self):
        self.cfgs = Configuration()
        self.dashboard = DataAnalyzerToolbox()
        self.data_fetch_callbacks = DataLoadingCallbacks(self.dashboard)
        self.data_overview_callbacks = DataOverviewCallbacks(self.dashboard)
        self.eda_callbacks = EdaCallbacks(self.dashboard)
        self.data_processing_callbacks = DataProcessingCallbacks(self.dashboard)
        self.feature_engineering_callbacks = FeatureEngineeringCallbacks(self.dashboard)
        self.train_evaluate_callbacks = TrainEvaluateCallbacks(self.dashboard)
        self.explainability_callbacks = ExplainabilityCallbacks(self.dashboard)

def main():
    """
    main function to initialize and run the dataset-analyzer-toolbox application.
    """
    app = DatasetAnalyzerApplication()
    app.data_fetch_callbacks.register_callbacks()
    app.data_overview_callbacks.register_callbacks()
    app.eda_callbacks.register_callbacks()
    app.data_processing_callbacks.register_callbacks()
    app.feature_engineering_callbacks.register_callbacks()
    app.train_evaluate_callbacks.register_callbacks()
    app.explainability_callbacks.register_callbacks()

    app.dashboard.app.run(
        debug=True,
        host=app.cfgs.system_host,
        port=app.cfgs.system_port
    )

if __name__ == '__main__':
    main()
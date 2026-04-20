from core.view.dataset_analyzer_toolbox import DatasetAnalyzerToolbox
from core.callbacks.data_loading import DataLoadingCallbacks
from core.callbacks.data_overview import DataOverviewCallbacks
from core.callbacks.eda import EdaCallbacks
from core.callbacks.data_processing import DataProcessingCallbacks
from core.callbacks.feature_engineering import FeatureEngineeringCallbacks
from core.callbacks.view_callbacks import ViewCallbacks
from configuration.configuration import Configuration

class DatasetAnalyzerApplication:
    def __init__(self):
        self.cfgs = Configuration()
        self.dashboard = DatasetAnalyzerToolbox()
        self.view_callbacks = ViewCallbacks(self.dashboard)
        self.data_loading_callbacks = DataLoadingCallbacks(self.dashboard)
        self.data_overview_callbacks = DataOverviewCallbacks(self.dashboard)
        self.eda_callbacks = EdaCallbacks(self.dashboard)
        self.data_processing_callbacks = DataProcessingCallbacks(self.dashboard)
        self.feature_engineering_callbacks = FeatureEngineeringCallbacks(self.dashboard)


def main():
    """
    main function to initialize and run the dataset-analyzer-toolbox application.
    """
    app = DatasetAnalyzerApplication()
    app.view_callbacks.register_callbacks()
    app.data_loading_callbacks.register_callbacks()
    app.data_overview_callbacks.register_callbacks()
    app.eda_callbacks.register_callbacks()
    app.data_processing_callbacks.register_callbacks()
    app.feature_engineering_callbacks.register_callbacks()

    app.dashboard.app.run(
        debug=True,
        host=app.cfgs.system_host,
        port=app.cfgs.system_port
    )

if __name__ == '__main__':
    main()
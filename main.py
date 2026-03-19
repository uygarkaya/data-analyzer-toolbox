from core.view.dataset_analyzer_toolbox import DatasetAnalyzerToolbox
from core.callbacks.core_callbacks import CoreCallbacks
from core.callbacks.view_callbacks import ViewCallbacks
from configuration.configuration import Configuration

class DatasetAnalyzerApplication:
    def __init__(self):
        self.cfgs = Configuration()
        self.dashboard = DatasetAnalyzerToolbox()
        self.core_callbacks = CoreCallbacks(self.dashboard)
        self.view_callbacks = ViewCallbacks(self.dashboard)


def main():
    """
    main function to initialize and run the dataset-analyzer-toolbox application.
    """
    app = DatasetAnalyzerApplication()
    app.view_callbacks.register_callbacks()
    app.core_callbacks.register_callbacks()
    app.dashboard.app.run(
        debug=True, 
        host=app.cfgs.system_host, 
        port=app.cfgs.system_port
    )

if __name__ == '__main__':
    main()
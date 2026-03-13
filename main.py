from core.view.dataset_analyzer_toolbox import DatasetAnalyzerToolbox
from configuration.configuration import Configuration

class DatasetAnalyzerApplication:
    def __init__(self):
        self.cfgs = Configuration()
        self.dashboard = DatasetAnalyzerToolbox()


def main():
    """
    main function to initialize and run the dataset-analyzer-toolbox application.
    """
    app = DatasetAnalyzerApplication()
    app.dashboard.app.run(
        debug=True, 
        host=app.cfgs.system_host, 
        port=app.cfgs.system_port
    )

if __name__ == '__main__':
    main()
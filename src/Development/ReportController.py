from src.Development.Training.LearningPlotModel import LearningPlotModel
from src.Development.Training.LearningPlotView import LearningPlotView
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig


class ReportController:
    LearningPlot = None
    ValidationReport = None
    TestReport = None

    def __init__(self) -> None:
        pass

    def create_learning_plot(self):
        db_conf = DBConfig('training', 'learning_plot')
        storage_controller = StorageController(db_conf, type(LearningPlotModel((0, 0, 0))))
        learning_plot_models = storage_controller.retrieve_all()
        print(learning_plot_models)
        # learning_plot_view = LearningPlotView('learning_plot', learning_plot_models[0])
        # learning_plot_view.update()


ReportController = ReportController()
ReportController.create_learning_plot()

from src.Development.LearningPlotModel import LearningPlotModel
from src.Development.LearningPlotView import LearningPlotView
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig


class ReportController:
    LearningPlot = None
    ValidationReport = None
    TestReport = None


def __init__() -> None:
    pass


def create_learning_plot():
    db_conf = DBConfig('training', 'learning_plot', ['loss', 'number_of_generations', 'loss_threshold'])
    storage_controller = StorageController(db_conf, type(None))
    learning_plot_model = LearningPlotModel(storage_controller)
    learning_plot_view = LearningPlotView('learning_plot', learning_plot_model)
    learning_plot_view.update()


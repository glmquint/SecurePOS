from src.Development.Training.LearningPlotModel import LearningPlotModel
from src.Development.Training.LearningPlotView import LearningPlotView
from src.Development.Validation.ValidationReportView import ValidationReportView
from src.Development.Testing.TestReportView import TestReportView
from src.Development.Validation.ValidationReportModel import ValidationReportModel
from src.Development.Testing.TestReportModel import TestReportModel
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig


class ReportController:
    db_confs : [DBConfig] = None

    def __init__(self) -> None:
        self.db_confs.append(DBConfig('training', 'learning_plot'))
        self.db_confs.append(DBConfig('validation', 'validation_report'))
        self.db_confs.append(DBConfig('testing', 'test_report'))

    def create_learning_plot(self):
        storage_controller = StorageController(self.db_confs[0], type(LearningPlotModel((0, 0, 0))))
        learning_plot_models = storage_controller.retrieve_all()
        print(learning_plot_models)
        learning_plot_view = LearningPlotView('learning_plot', learning_plot_models[0])  # use the first model
        learning_plot_view.update()

    def create_validation_report(self):
        storage_controller = StorageController(self.db_confs[1], type(ValidationReportModel((0, 0, 0))))
        validation_report_models = storage_controller.retrieve_all()
        print(validation_report_models)
        validation_report_view = ValidationReportView('validation_report', validation_report_models)
        validation_report_view.update()

    def create_test_report(self):
        storage_controller = StorageController(self.db_confs[2], type(TestReportModel((0, 0, 0))))
        test_report_models = storage_controller.retrieve_all()
        print(test_report_models)
        test_report_view = TestReportView('test_report', test_report_models)
        test_report_view.update()


#ReportController = ReportController()
#ReportController.create_learning_plot()

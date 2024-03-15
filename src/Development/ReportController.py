from src.Development.Training.LearningPlotModel import LearningPlotModel
from src.Development.Training.LearningPlotView import LearningPlotView
from src.Development.Validation.ValidationReportView import ValidationReportView
from src.Development.Testing.TestReportView import TestReportView
from src.Development.Validation.ValidationReportModel import ValidationReportModel
from src.Development.Testing.TestReportModel import TestReportModel
from src.MessageBus.MessageBus import MessageBus


class ReportController:
    message_bus: MessageBus = None

    def __init__(self, message_bus: MessageBus) -> None:
        self.message_bus = message_bus

    def create_learning_plot(self):
        data = self.message_bus.popTopic("learning_plot")
        learning_plot_model = LearningPlotModel(data[0], data[1], data[2])
        learning_plot_view = LearningPlotView('learning_plot', learning_plot_model)
        learning_plot_view.update()

    def create_validation_report(self):
        scoreboard = self.message_bus.popTopic("Scoreboard")
        validation_report_model = ValidationReportModel(scoreboard)
        validation_report_view = ValidationReportView('Validation', validation_report_model)
        validation_report_view.update()

    def create_test_report(self):
        test_report_data = self.message_bus.popTopic("test_report")
        test_report_model = TestReportModel(test_report_data[0], test_report_data[1], test_report_data[2],
                                            test_report_data[3])
        test_report_view = TestReportView('test_report', test_report_model)
        test_report_view.update()

# ReportController = ReportController()
# ReportController.create_learning_plot()

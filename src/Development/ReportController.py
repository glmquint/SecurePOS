import os

from src.Development.Training.LearningPlotModel import LearningPlotModel
from src.Development.Training.LearningPlotView import LearningPlotView
from src.Development.Validation.ValidationReportView import ValidationReportView
from src.Development.Testing.TestReportView import TestReportView
from src.Development.Validation.ValidationReportModel import ValidationReportModel
from src.Development.Testing.TestReportModel import TestReportModel
from src.MessageBus.MessageBus import MessageBus


class ReportController:
    """
    A class used to control the reports in the development system.

    Attributes
    ----------
    message_bus : MessageBus
        The message bus for the system.

    Methods
    -------
    __init__(self, message_bus: MessageBus)
        Initializes the ReportController class.
    create_learning_plot(self)
        Creates a learning plot and updates the view.
    create_validation_report(self)
        Creates a validation report and updates the view.
    create_test_report(self)
        Creates a test report and updates the view.
    """
    # class implementation...class ReportController:
    message_bus: MessageBus = None

    def __init__(self, message_bus: MessageBus) -> None:
        self.message_bus = message_bus

    def create_learning_plot(self):
        print(f'[{self.__class__.__name__}]: creating learning plot')
        data = self.message_bus.popTopic("learning_plot")
        learning_plot_model = LearningPlotModel(data[0], data[1], data[2])
        learning_plot_view = LearningPlotView(
            'learning_plot', learning_plot_model)
        learning_plot_view.update()
        print(f'[{self.__class__.__name__}]: learning plot created')

    def create_validation_report(self):
        print(f'[{self.__class__.__name__}]: creating validation report')
        scoreboard = self.message_bus.popTopic("Scoreboard")
        validation_report_model = ValidationReportModel(scoreboard)
        validation_report_view = ValidationReportView(
            f'{os.path.dirname(__file__)}/Validation',
            validation_report_model)
        validation_report_view.update()
        print(f'[{self.__class__.__name__}]: validation report created')

    def create_test_report(self):
        print(f'[{self.__class__.__name__}]: creating test report')
        test_report_data = self.message_bus.popTopic("test_report")
        test_report_model = TestReportModel(
            test_report_data[0],
            test_report_data[1],
            test_report_data[2],
            test_report_data[3])
        test_report_view = TestReportView('test_report', test_report_model)
        test_report_view.update()
        print(f'[{self.__class__.__name__}]: test report created')

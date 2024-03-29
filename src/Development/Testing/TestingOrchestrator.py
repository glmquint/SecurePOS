import json
import os
import random

from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.ReportController import ReportController
from src.Development.Training.TrainProcess import TrainProcess
from src.JsonIO.JsonValidator import JSONValidator
from src.MessageBus.MessageBus import MessageBus


class TestingOrchestrator:
    """
        A class used to orchestrate the testing process in the development system.

        Attributes
        ----------
        training_process : TrainProcess
            The process responsible for the training of the classifiers.
        report_controller : ReportController
            The controller responsible for generating reports.
        message_bus : MessageBus
            The message bus used for inter-process communication.
        configurations : DevelopmentSystemConfigurations
            The configurations for the development system.

        Methods
        -------
        __init__(self, status: DevelopmentSystemStatus, report_controller: ReportController, message_bus: MessageBus, configurations: DevelopmentSystemConfigurations)
            Initializes the TestingOrchestrator class with the status, report controller, message bus, and configurations.
        check_test_result(self) -> int
            Checks the test result and returns an integer indicating the result.
        start(self)
            Starts the testing process.
    """
    training_process: TrainProcess = None
    report_controller: ReportController = None
    message_bus: MessageBus = None
    configurations: DevelopmentSystemConfigurations = None

    def __init__(
            self,
            status: DevelopmentSystemStatus,
            report_controller: ReportController,
            message_bus: MessageBus,
            configurations: DevelopmentSystemConfigurations):
        self.report_controller = report_controller
        self.message_bus = message_bus
        self.status = status
        self.configurations = configurations
        self.training_process = TrainProcess(
            self.status, self.message_bus, self.configurations)

    def check_test_result(self) -> int:
        ret_val = -1
        try:
            with open(f'{os.path.dirname(__file__)}/test_result.json', 'r', encoding='utf-8') as json_file:
                ret_val = 0
                data = json.load(json_file)
                JSONValidator(
                    f"{os.path.dirname(__file__)}/../schema/result_schema.json").validate_data(data)
                if data['result'] in [""]:
                    ret_val = -1
                elif data['result'] in ["ok", "OK", "Ok"]:
                    ret_val = 1
        except FileNotFoundError:  # create file so that AI expert can fill it
            with open(f'{os.path.dirname(__file__)}/test_result.json', 'w', encoding='utf-8') as json_file:
                json.dump({"result": ""}, json_file)
        finally:
            return ret_val

    def start(self):
        while True:
            if self.status.status == "generate_test_report":
                self.training_process.test_classifier()
                self.report_controller.create_test_report()
                self.status.status = "check_test_report"
            elif self.status.status == "check_test_report":
                if self.configurations.stop_and_go:
                    response = self.check_test_result()
                else:
                    response = random.randint(1, 1)  # response is always good
                if response < 0:
                    self.status.save_status()
                elif response == 0:
                    self.status.status = "send_config"
                    self.training_process.remove_precedent_response(
                        f'{os.path.dirname(__file__)}/../Validation/validation_result')
                    self.training_process.remove_precedent_response(
                        f'{os.path.dirname(__file__)}/../Training/learning_result')
                    self.training_process.remove_precedent_response(
                        f'{os.path.dirname(__file__)}/../Training/number_of_iterations')
                    self.training_process.remove_precedent_response(
                        f'{os.path.dirname(__file__)}/../Testing/test_result')
                elif response == 1:
                    self.status.status = "send_classifier"
                break
            else:
                raise Exception("Invalid status")

import json
import os
import random

from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.ReportController import ReportController
from src.Development.Training.TrainProcess import TrainProcess
from src.JsonIO.JsonValidator import JSONValidator
from src.MessageBus.MessageBus import MessageBus


class ValidationOrchestrator:
    """
    A class used to orchestrate the validation process in the development system.

    Attributes
    ----------
    report_controller : ReportController
        The controller for the reports.
    message_bus : MessageBus
        The message bus for the system.
    status : DevelopmentSystemStatus
        The status of the development system.
    configurations : DevelopmentSystemConfigurations
        The configurations for the development system.
    training_process : TrainProcess
        The process for training.

    Methods
    -------
    __init__(self, status: DevelopmentSystemStatus, report_controller: ReportController, message_bus: MessageBus, configurations: DevelopmentSystemConfigurations)
        Initializes the ValidationOrchestrator class.
    check_validation_result(self) -> int
        Checks the validation result and returns an integer based on the result.
    start(self)
        Starts the orchestrator and manages the operations based on the system status.
    """
    # class implementation...class ValidationOrchestrator:
    report_controller: ReportController = None
    message_bus: MessageBus = None
    status: DevelopmentSystemStatus = None
    configurations: DevelopmentSystemConfigurations = None
    training_process: TrainProcess = None

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
        self.training_process = TrainProcess(self.status, self.message_bus,
                                             self.configurations)

    def check_validation_result(self) -> int:
        ret_val = -1
        try:
            with open(f'{os.path.dirname(__file__)}/validation_result.json', 'r') as json_file:
                ret_val = 0
                data = json.load(json_file)
                JSONValidator(
                    f"{os.path.dirname(__file__)}/../schema/result_schema.json").validate_data(data)
                if data['result'] in [""]:
                    ret_val = -1  # AI expert has not filled the file
                elif data['result'] in ["ok", "OK", "Ok", "oK"]:
                    ret_val = 1
        except FileNotFoundError as e:  # create file so that AI expert can fill it
            with open(f'{os.path.dirname(__file__)}/validation_result.json', 'w') as json_file:
                json.dump({"result": ""}, json_file)
        finally:
            return ret_val

    def start(self):
        while True:
            if self.status.status == "set_hyperparams":
                self.training_process.set_hyperparams()
                self.status.should_validate = True
                self.status.status = "do_grid_search"
            if self.status.status == "do_grid_search":
                self.training_process.perform_grid_search()
                self.status.should_validate = False
                self.status.status = "generate_validation_report"
            elif self.status.status == "generate_validation_report":
                self.report_controller.create_validation_report()
                self.status.status = "check_validation_report"
            elif self.status.status == "check_validation_report":
                if self.configurations.stop_and_go:
                    response = self.check_validation_result()
                else:
                    response = random.randint(1, 1)  # response is always good
                if self.status.best_classifier_name == "Invalid":  # if no best classifier repeat the process
                    response = 0
                    print(
                        f'[{self.__class__.__name__}]: no valid classifier from validation, overriding user choice')
                if response < 0:
                    self.status.status = "check_validation_report"
                    self.status.save_status()
                elif response == 0:  # no valid classifier, repeat the process
                    self.status.status = "set_avg_hyperparams"
                    self.training_process.remove_classifiers(
                        f'{os.path.dirname(__file__)}/../classifiers')
                    self.training_process.remove_precedent_response(
                        f'{os.path.dirname(__file__)}/validation_result')
                    self.training_process.remove_precedent_response(
                        f'{os.path.dirname(__file__)}/../Training/learning_result')
                    self.training_process.remove_precedent_response(
                        f'{os.path.dirname(__file__)}/../Training/number_of_iterations')
                    if self.configurations.stop_and_go:
                        self.status.save_status()
                    else:
                        break
                elif response == 1:
                    self.status.status = "generate_test_report"
                    break
            else:
                raise Exception("Invalid status")

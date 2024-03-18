import json
import random

from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.ReportController import ReportController
from src.Development.Training.TrainProcess import TrainProcess
from src.JsonIO.JsonValidator import JSONValidator
from src.MessageBus.MessageBus import MessageBus


class ValidationOrchestrator:
    report_controller: ReportController = None
    message_bus: MessageBus = None
    status: DevelopmentSystemStatus = None
    configurations: DevelopmentSystemConfigurations = None
    grid_search = None
    trainining_process: TrainProcess = None

    def __init__(self, status: DevelopmentSystemStatus, report_controller: ReportController, message_bus: MessageBus,
                 configurations: DevelopmentSystemConfigurations):
        self.report_controller = report_controller
        self.message_bus = message_bus
        self.status = status
        self.configurations = configurations
        self.trainining_process = TrainProcess(self.status, self.message_bus,
                                               self.configurations)

    def check_validation_result(self) -> int:
        ret_val = -1
        try:
            with open('Validation/validation_result.json', 'r') as json_file:
                ret_val = 0
                data = json.load(json_file)
                JSONValidator("schema/result_schema.json").validate_data(data)
                if data['result'] in [""]:
                    ret_val = -1  # AI expert has not filled the file
                elif data['result'] in ["ok", "OK", "Ok", "oK"]:
                    ret_val = 1
        except FileNotFoundError as e:  # create file so that AI expert can fill it
            with open('Validation/validation_result.json', 'w') as json_file:
                json.dump({"result": ""}, json_file)
        finally:
            return ret_val

    def start(self):
        while True:
            if self.status.status == "set_hyperparams":
                self.trainining_process.set_hyperparams()
                self.status.should_validate = True
                self.status.status = "do_grid_search"
            if self.status.status == "do_grid_search":
                self.trainining_process.perform_grid_search()
                self.status.should_validate = False
                self.status.status = "generate_validation_report"
            elif self.status.status == "generate_validation_report":
                self.report_controller.create_validation_report()
                self.status.status = "check_validation_report"
            elif self.status.status == "check_validation_report":
                if self.configurations.stop_and_go:
                    response = self.check_validation_result()
                else:
                    response = random.randint(0, 1)
                if response < 0:
                    self.status.status = "check_validation_report"
                    self.status.save_status()
                elif response == 0:  # no valid classifier, repeat the process
                    self.status.status = "set_avg_hyperparams"
                    self.trainining_process.remove_classifiers('classifiers')
                    self.trainining_process.remove_precedent_response('Validation/validation_result')
                    self.trainining_process.remove_precedent_response('Training/learning_result')
                    self.trainining_process.remove_precedent_response('Training/number_of_iterations')
                    if self.configurations.stop_and_go:
                        self.status.save_status()
                    else:
                        break
                elif response == 1:
                    self.status.status = "generate_test_report"
                    break
            else:
                raise Exception("Invalid status")

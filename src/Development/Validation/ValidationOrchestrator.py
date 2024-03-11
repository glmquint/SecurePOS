import itertools
import json

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
                JSONValidator.validate_data(data, "schema/result_schema.json")
                if data['result'] in ["ok", "OK", "Ok"]:
                    ret_val = 1
        except FileNotFoundError as e:  # create file so that AI expert can fill it
            with open('Validation/validation_result.json', 'w') as json_file:
                json.dump({"result": ""}, json_file)
        finally:
            return ret_val

    def start(self):
        while True:
            if self.status.status == "do_grid_search":
                self.trainining_process.start()
                self.status.status = "generate_validation_report"
            elif self.status.status == "generate_validation_report":
                self.report_controller.create_validation_report()
                self.status.status = "check_validation_report"
            elif self.status.status == "check_validation_report":
                response = self.check_validation_result()
                if response == 0:
                    self.status.status = "set_avg_hyperparams"
                elif response == 1:
                    self.status.status = "generate_test_report"
                self.status.save_status()
                break  # response -1 is handled, close the application
            else:
                raise Exception("Invalid status")

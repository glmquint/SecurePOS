import json

from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.ReportController import ReportController
from src.MessageBus.MessageBus import MessageBus


class ValidationOrchestrator:
    report_controller: ReportController = None
    message_bus: MessageBus = None
    status: DevelopmentSystemStatus = None

    def __init__(self, status: DevelopmentSystemStatus, report_controller: ReportController, message_bus: MessageBus):
        self.report_controller = report_controller
        self.message_bus = message_bus
        self.status = status

    def check_validation_result(self) -> int:
        ret_val = -1
        with open('validation_report.json', 'r') as json_file:  # validate learning_result.json
            ret_val = 0
            data = json.load(json_file)
            if data['result'] in ["ok", "OK", "Ok"]:
                ret_val = 1
        return ret_val

    def set_hyperparameters(self):
        return None

    def start(self):
        while True:
            if self.status.status == "set_hyperparam":
                next_hyperparam = self.set_hyperparameters()
                if next_hyperparam:
                    self.status.status = "train"
                    self.status.should_validate = True
                    self.status.save_status()
                    break
                else:  # if empty grid hyperparameter remember to set the status to should_validate=False
                    self.status.status = "generate_validation_report",
                    self.status.should_validate = False
                    self.status.save_status()
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

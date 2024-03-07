import json

from src.Development.DevSystemStatus import DevSystemStatus
from src.Development.ReportController import ReportController
from src.MessageBus.MessageBus import MessageBus


class ValidationOrchestrator:
    report_controller: ReportController = None
    message_bus: MessageBus = None

    def __init__(self, status: DevSystemStatus, report_controller: ReportController, message_bus: MessageBus):
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
                    self.status.save_status("train", True)
                    break
                else:  # if empty grid hyperparameter remember to set the status to should_validate=False
                    self.status.save_status("generate_validation_report", False)
            elif self.status.status == "generate_validation_report":
                self.report_controller.create_validation_report()
                self.status.save_status("check_validation_report", False)
            elif self.status.status == "check_validation_report":
                response = self.check_validation_result()
                if response == 0:
                    self.status.save_status("set_avg_hyperparam", False)
                elif response == 1:
                    self.status.save_status("generate_test_report", False)

                break  # response -1 is handled, close the application
            else:
                raise Exception("Invalid status")

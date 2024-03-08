import json

from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.ReportController import ReportController
from src.JsonIO.JsonValidator import JSONValidator
from src.MessageBus.MessageBus import MessageBus


class TestingOrchestrator:
    report_controller: ReportController = None
    message_bus: MessageBus = None

    def __init__(self, status: DevelopmentSystemStatus, report_controller: ReportController, message_bus: MessageBus):
        self.report_controller = report_controller
        self.message_bus = message_bus
        self.status = status

    def check_test_result(self) -> int:
        ret_val = -1
        try:
            with open('Testing/test_result.json', 'r') as json_file:
                ret_val = 0
                data = json.load(json_file)
                JSONValidator("schema/result_schema.json").validate_data(data)
                if data['result'] in ["ok", "OK", "Ok"]:
                    ret_val = 1
        except FileNotFoundError as e:  # create file so that AI expert can fill it
            with open('Testing/test_result.json', 'w') as json_file:
                json.dump({"result": ""}, json_file)
        finally:
            return ret_val

    def start(self):
        while True:
            if self.status.status == "generate_test_report":
                self.report_controller.create_test_report()
                self.status.status = "check_test_report"
            elif self.status.status == "check_test_report":
                response = self.check_test_result()
                if response == 0:
                    self.status.status = "send_config"
                elif response == 1:
                    self.status.status = "send_classifier"
                self.status.save_status()
                break  # response -1 is handled, close the application
            else:
                raise Exception("Invalid status")

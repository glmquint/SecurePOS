import json

from src.Development.DevSystemStatus import DevSystemStatus
from src.Development.ReportController import ReportController
from src.MessageBus.MessageBus import MessageBus


class TestingOrchestrator:
    report_controller: ReportController = None
    message_bus: MessageBus = None

    def __init__(self, status: DevSystemStatus, report_controller: ReportController, message_bus: MessageBus):
        self.report_controller = report_controller
        self.message_bus = message_bus
        self.status = status

    def check_test_result(self) -> int:
        ret_value = -1
        with open('test_result.json', 'r') as json_file:  # validate test_result.json
            ret_value = 0
            data = json.load(json_file)
            if data['result'] in ["ok", "OK", "Ok"]:
                ret_value = 1
        return ret_value

    def start(self):
        while True:
            if self.status.status == "generate_test_report":
                self.report_controller.create_test_report()
                self.status.save_status("check_test_report", False)
            elif self.status.status == "check_test_report":
                response = self.check_test_result()
                if response == 0:
                    self.status.save_status("send_config", False)
                elif response == 1:
                    self.status.save_status("send_classifier", False)
                break  # response -1 is handled, close the application
            else:
                raise Exception("Invalid status")



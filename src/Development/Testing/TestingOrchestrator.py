import json

from src.Development.ReportController import ReportController
from src.MessageBus.MessageBus import MessageBus


class TestingOrchestrator:
    report_controller: ReportController = None
    message_bus: MessageBus = None

    def __init__(self, report_controller: ReportController, message_bus: MessageBus):
        self.report_controller = report_controller
        self.message_bus = message_bus

    def check_test_result(self) -> bool:
        input("> Please insert the decision in test_result.json file")
        with open('test_result.json', 'r') as json_file:  # validate test_result.json
            data = json.load(json_file)
            return data['result'] == "OK"

    def start(self):
        self.report_controller.create_test_report()
        return self.check_test_result()

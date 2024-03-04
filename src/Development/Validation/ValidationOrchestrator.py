import json

from src.Development.ReportController import ReportController
from src.MessageBus.MessageBus import MessageBus


class ValidationOrchestrator:
    report_controller: ReportController = None
    message_bus: MessageBus = None

    def __init__(self, report_controller: ReportController, message_bus: MessageBus):
        self.report_controller = report_controller
        self.message_bus = message_bus

    def check_validation_result(self):
        input("> Please insert the decision in validation_result.json file")
        with open('validation_report.json', 'r') as json_file:  # validate validation_result.json
            data = json.load(json_file)
            return data['result'] == "OK"


    def start(self):
        self.report_controller.create_validation_report()
        return self.check_validation_result()

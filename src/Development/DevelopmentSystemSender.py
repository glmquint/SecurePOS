from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.JsonIO.FileSender import FileSender
from src.JsonIO.JSONSender import JSONSender


class DevelopmentSystemSender:
    messaging_sender: JSONSender = None
    production_sender: FileSender = None
    development_system_configurations: DevelopmentSystemConfigurations = None
    status: DevelopmentSystemStatus = None

    def __init__(self, development_system_configurations: DevelopmentSystemConfigurations, status: DevelopmentSystemStatus):
        self.development_system_configurations = development_system_configurations
        self.messaging_sender = JSONSender('schema/config_schema.json', self.development_system_configurations.messaging_system_receiver)
        self.production_sender = FileSender(self.development_system_configurations.production_system_receiver)
        self.status = status

    def send_to_messaging(self):
        self.messaging_sender.send(self.development_system_configurations.to_dict())

    def send_to_production(self):
        with open(f'Training/{self.status.best_classifier_name}.sav', 'rb') as file:
            self.production_sender.send(file)
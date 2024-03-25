import os

from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.JsonIO.FileSender import FileSender
from src.JsonIO.JSONSender import JSONSender
from src.util import monitorPerformance


class DevelopmentSystemSender:
    messaging_sender: JSONSender = None
    production_sender: FileSender = None
    development_system_configurations: DevelopmentSystemConfigurations = None
    status: DevelopmentSystemStatus = None

    def __init__(self, development_system_configurations: DevelopmentSystemConfigurations,
                 status: DevelopmentSystemStatus):
        self.development_system_configurations = development_system_configurations
        self.messaging_sender = JSONSender(
            f'{os.path.dirname(__file__)}/schema/config_schema.json',
            self.development_system_configurations.messaging_system_receiver)
        self.production_sender = FileSender(self.development_system_configurations.production_system_receiver)
        self.status = status

    @monitorPerformance(should_sample_after=True)
    def send_to_messaging(self):
        self.messaging_sender.send(self.development_system_configurations.to_dict())

    @monitorPerformance(should_sample_after=True)
    def send_to_production(self):
        print(f'[{self.__class__.__name__}]: Sending classifier to production')
        with open(f'{os.path.dirname(__file__)}/classifiers/{self.status.best_classifier_name}.sav', 'rb') as file:
            self.production_sender.send(file)

import json
import os

from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.JsonIO.FileSender import FileSender
from src.JsonIO.JSONSender import JSONSender
from src.util import monitorPerformance, Message


class DevelopmentSystemSender:
    """
    A class used to handle the sending operations of the development system.

    Attributes
    ----------
    messaging_sender : JSONSender
        The sender for the messaging system.
    production_sender : FileSender
        The sender for the production system.
    development_system_configurations : DevelopmentSystemConfigurations
        The configurations for the development system.
    status : DevelopmentSystemStatus
        The status of the development system.

    Methods
    -------
    __init__(self, development_system_configurations: DevelopmentSystemConfigurations, status: DevelopmentSystemStatus)
        Initializes the DevelopmentSystemSender class.
    send_to_messaging(self)
        Sends the development system configurations to the messaging system.
    send_to_production(self)
        Sends the best classifier to the production system.
    """
    # class implementation...
    messaging_sender: JSONSender = None
    production_sender: FileSender = None
    development_system_configurations: DevelopmentSystemConfigurations = None
    status: DevelopmentSystemStatus = None

    def __init__(
            self,
            development_system_configurations: DevelopmentSystemConfigurations,
            status: DevelopmentSystemStatus):
        self.development_system_configurations = development_system_configurations
        self.messaging_sender = JSONSender(
            f'{os.path.dirname(__file__)}/../DataObjects/Schema/MessageSchema.json',
            self.development_system_configurations.messaging_system_receiver)
        self.production_sender = FileSender(
            self.development_system_configurations.production_system_receiver)
        self.status = status

    @monitorPerformance(should_sample_after=True)
    def send_to_messaging(self):
        self.messaging_sender.send(
            Message(
                msg=json.dumps(
                    self.development_system_configurations.to_dict())))

    @monitorPerformance(should_sample_after=True)
    def send_to_production(self):
        print(f'[{self.__class__.__name__}]: Sending classifier to production')
        with open(f'{os.path.dirname(__file__)}/classifiers/{self.status.best_classifier_name}.sav', 'rb') as file:
            self.production_sender.send(file)

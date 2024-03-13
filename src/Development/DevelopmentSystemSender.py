from src.JsonIO.FileSender import FileSender
from src.JsonIO.JSONSender import JSONSender
from src.Development.Classifier import Classifier


class DevelopmentSystemSender:
    messaging_sender: JSONSender = None
    production_sender: FileSender = None

    def __init__(self, url_messaging: str, url_production: str):
        self.messaging_sender = JSONSender('schema/config_schema.json', url_messaging)
        self.production_sender = FileSender(url_production)

    def send_to_messaging(self, Config):
        self.messaging_sender.send(Config.toJSON())

    def send_to_production(self):
        with open('Training/classifier.sav', 'rb') as file:
            self.production_sender.send(file)

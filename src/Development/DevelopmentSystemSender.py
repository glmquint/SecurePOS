from src.JsonIO.JSONSender import JSONSender
from src.DataObjects.Classifier import Classifier


class DevelopmentSystemSender:
    messaging_sender: JSONSender = None
    production_sender: JSONSender = None

    def __init__(self, url_messaging: str, url_production: str):
        self.messaging_sender = JSONSender('../../json_schema/config_schema.json', url_messaging)
        self.production_sender = JSONSender('../../json_schema/classifier_schema.json.json', url_production)

    def send_to_messaging(self, Config):
        self.messaging_sender.send(Config.toJSON())

    def send_to_production(self, classifier: Classifier):
        self.production_sender.send(classifier.toJSON())

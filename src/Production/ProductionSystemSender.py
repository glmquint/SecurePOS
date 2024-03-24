import os

from src.JsonIO.JSONSender import JSONSender
from src.util import monitorPerformance


class ProductionSystemSender:
    def __init__(self, message_url, evaluation_url, client_url):
        self.message_url = message_url
        self.evaluation_url = evaluation_url
        self.client_url = client_url

    @monitorPerformance(should_sample_after=True)
    def sendToMessaging(self, message):
        #TODO: fix schema for message
        sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/AttackRiskLabelSchema.json",
                            self.message_url)
        sender.send(message)

    @monitorPerformance(should_sample_after=True)
    def sendToEvaluation(self, label):
        sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/AttackRiskLabelSchema.json",
                            self.evaluation_url)
        self.send(self.evaluation_url, label)

    @monitorPerformance(should_sample_after=True)
    def sendToClient(self, label):
        sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/AttackRiskLabelSchema.json",
                            self.client_url)
        self.send(self.evaluation_url, label)
import os

from src.JsonIO.JSONSender import JSONSender
from src.util import monitorPerformance


class ProductionSystemSender:
    def __init__(self, message_url, evaluation_url, client_url):
        self.message_url = message_url
        self.evaluation_url = evaluation_url
        self.client_url = client_url
        #TODO: fix schema for message
        self.messaging_sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/MessageSchema.json",
                                           self.message_url)
        self.eval_sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/AttackRiskLabelSchema.json",
                                      self.evaluation_url)
        self.client_sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/AttackRiskLabelSchema.json",
                                        self.client_url)

    @monitorPerformance(should_sample_after=True)
    def sendToMessaging(self, message):
        self.messaging_sender.send(message)

    @monitorPerformance(should_sample_after=True)
    def sendToEvaluation(self, label):
        self.eval_sender.send(label)

    @monitorPerformance(should_sample_after=True)
    def sendToClient(self, label):
        self.client_sender.send(label)
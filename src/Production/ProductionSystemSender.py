import os

from src.JsonIO.JSONSender import JSONSender
from src.util import monitorPerformance


class ProductionSystemSender:
    """
    This class is responsible for sending messages, labels to the messaging, evaluation, and client URLs respectively.
    It uses JSONSender to send the data.

    Attributes:
        message_url: The URL for sending messages.
        evaluation_url: The URL for sending evaluation labels.
        client_url: The URL for sending labels to the client.
        messaging_sender: An object that sends messages to the message_url.
        eval_sender: An object that sends labels to the evaluation_url.
        client_sender: An object that sends labels to the client_url.
    """
    def __init__(self, message_url, evaluation_url, client_url):
        self.message_url = message_url
        self.evaluation_url = evaluation_url
        self.client_url = client_url
        self.messaging_sender = JSONSender(
            f"{os.path.dirname(__file__)}/../DataObjects/Schema/MessageSchema.json",
            self.message_url)
        self.eval_sender = JSONSender(
            f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json",
            self.evaluation_url)
        self.client_sender = JSONSender(
            f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json",
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

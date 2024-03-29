import os

from src.Evaluation.EvaluationSystemConfig import EvaluationSystemConfig
from src.JsonIO.JSONSender import JSONSender
from src.util import monitorPerformance


class EvaluationSystemSender:
    """
        This class is responsible for sending messages to the messaging system. It initializes the sender with a configuration
        and sends messages to the messaging system.

        Attributes:
            message_url: The URL of the messaging system.
            messaging_sender: An object of JSONSender that handles the sending of messages.

        Methods:
            sendtomessaging: Sends a message to the messaging system.
    """
    def __init__(self, config: EvaluationSystemConfig):

        self.message_url = f"http://{config.messaging_ip}:{config.messaging_port}/messaging_system"

        self.messaging_sender = JSONSender(
            f"{os.path.dirname(__file__)}/../DataObjects/Schema/MessageSchema.json",
            self.message_url)

    @monitorPerformance(should_sample_after=True)
    def sendtomessaging(self, message):
        """send message"""
        self.messaging_sender.send(message)

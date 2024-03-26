import os

from src.JsonIO.JSONSender import JSONSender, JSONValidator
from src.util import monitorPerformance, Message


class EvaluationSystemSender:
    def __init__(self):
        #sender = JSONSender(f"{os.path.dirname(__file__)}/../MessagingSystem/Schema/Label.json", "http://127.0.0.1:6000/messaging_system")
        #todo fix to be loaded from config
        self.message_url = "http://127.0.0.1:6000/messaging_system"
        # TODO: fix schema for message
        self.messaging_sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/AttackRiskLabelSchema.json",
                                           self.message_url)

    @monitorPerformance(should_sample_after=True)
    def sendtomessaging(self,message):
        self.messaging_sender.send(message)
        return

#s = EvaluationSystemSender()
#s.sendtomessaging(Message(msg = "BYPASS DI MERDA"))
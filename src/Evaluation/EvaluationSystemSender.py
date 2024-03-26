import os

from src.Evaluation.EvaluationSystemConfig import EvaluationSystemConfig
from src.JsonIO.JSONSender import JSONSender, JSONValidator
from src.util import monitorPerformance, Message


class EvaluationSystemSender:
    def __init__(self,config: EvaluationSystemConfig):
        #sender = JSONSender(f"{os.path.dirname(__file__)}/../MessagingSystem/Schema/Label.json", "http://127.0.0.1:6000/messaging_system")

        self.message_url = f"http://{config.messaging_ip}:{config.messaging_port}/messaging_system"

        self.messaging_sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/MessageSchema.json",
                                           self.message_url)

    @monitorPerformance(should_sample_after=True)
    def sendtomessaging(self,message):
        self.messaging_sender.send(message)
        return

#s = EvaluationSystemSender()
#s.sendtomessaging(Message(msg = "BYPASS DI MERDA"))
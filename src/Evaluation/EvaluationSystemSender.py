import os

from src.JsonIO.JSONSender import JSONSender, JSONValidator
from src.util import monitorPerformance


class EvaluationSystemSender:
    def __init__(self):
        sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json", "http://127.0.0.1:6000/messaging_system")
        return

    @monitorPerformance(should_sample_after=True)
    def sendtomessaging(self,config):
        self.sender.send({"attackRiskLabel": "low"})
        return

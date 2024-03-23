from src.JsonIO.JSONSender import JSONSender, JSONValidator



class EvaluationSystemSender:
    def __init__(self):
        sender = JSONSender("../DataObjects/Schema/Label.json", "http://localhost:6000/messaging_system")
        return

    def sendtomessaging(self,config):
        self.sender.send({"attackRiskLabel": "low"})
        return

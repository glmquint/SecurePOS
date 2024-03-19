from src.JsonIO.JSONSender import JSONSender, JSONValidator



class EvaluationSystemSender:
    def __init__(self):
        sender = JSONSender("../DataObjects/Schema/Label.json", "http://127.0.0.1:5000/test_endpoint")
        return

    def sendtomessaging(self,config):
        self.sender.send({"attackRiskLabel": "low"})
        return

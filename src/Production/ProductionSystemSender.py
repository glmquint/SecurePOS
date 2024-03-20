from src.JsonIO.JSONSender import JSONSender


class ProductionSystemSender:
    def __init__(self):
        pass


    def send(self, url, label):
        sender = JSONSender("../DataObjects/Schema/AttackRiskLabelSchema.json", url)
        sender.send(label)
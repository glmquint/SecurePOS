from src.JsonIO.JSONSender import JSONSender


class ProductionSystemSender:
    def __init__(self, attackRiskLabel):
        self.attackRiskLabel = attackRiskLabel

    def send(self, url):
        sender = JSONSender("../DataObjects/Schema/AttackRiskLabelSchema.json", url)
        sender.send(self.attackRiskLabel.to_json())
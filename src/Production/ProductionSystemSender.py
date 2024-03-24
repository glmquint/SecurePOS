import os

from src.JsonIO.JSONSender import JSONSender
from src.util import monitorPerformance


class ProductionSystemSender:
    def __init__(self):
        pass

    @monitorPerformance(should_sample_after=True)
    def send(self, url, label):
        sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/AttackRiskLabelSchema.json", url)
        sender.send(label)

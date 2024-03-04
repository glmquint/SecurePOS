import time

from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server

sender = JSONSender("../DataObjects/Schema/AttackRiskLabelSchema.json", "http://127.0.0.1:5000/test_endpoint")
sender.send({"attackRiskLabel": "low"})
time.sleep(1)
sender.send({"attackRiskLabel": "high"})
time.sleep(4)
sender.send({"attackRiskLabel": "medium"})
time.sleep(1)
sender.send({"attackRiskLabel": "low"})
#assert sender.send({"invalid": "low"}) == False

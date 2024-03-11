import time

from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server

sender2 = JSONSender("../DataObjects/Schema/AttackRiskLabelSchema.json", "http://127.0.0.1:5000/security_expert_endpoint")
sender = JSONSender("../DataObjects/Schema/AttackRiskLabelSchema.json", "http://127.0.0.1:5000/label_endpoint")

sender2.send({"attackRiskLabel": "high"})
sender.send({"attackRiskLabel": "low"})
sender2.send({"attackRiskLabel": "medium"})
sender.send({"attackRiskLabel": "low"})

sender.send({"attackRiskLabel": "low"})
sender2.send({"attackRiskLabel": "high"})
sender2.send({"attackRiskLabel": "medium"})
sender.send({"attackRiskLabel": "low"})

sender.send({"attackRiskLabel": "low"})
sender2.send({"attackRiskLabel": "high"})

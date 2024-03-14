import time
from asyncio import wait
from random import randint

from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server


sender2 = JSONSender("../DataObjects/Schema/AttackRiskLabelSchema.json", "http://127.0.0.1:5000/security_expert_endpoint")
sender = JSONSender("../DataObjects/Schema/AttackRiskLabelSchema.json", "http://127.0.0.1:5000/label_endpoint")
for x in range(0,55):
    #print(x)
    y = randint(1,2)
    x = randint(1,20)
    if y == 1:
        st = "high"
    elif y == 2:
        st = "medium"
    elif y == 3:
        st = "low"
    st2 = st
    if x == 10:
        st2 = "high"
    elif x == 2:
        st2 = "medium"
    elif x == 3:
        st2 = "low"
    sender2.send({"attackRiskLabel": st2})
    sender.send({"attackRiskLabel": st})
time.sleep(1)
exit()
sender2.send({"attackRiskLabel": "medium"})
sender.send({"attackRiskLabel": "low"})

sender.send({"attackRiskLabel": "low"})
sender2.send({"attackRiskLabel": "high"})
sender2.send({"attackRiskLabel": "medium"})
sender.send({"attackRiskLabel": "low"})

sender.send({"attackRiskLabel": "low"})
sender2.send({"attackRiskLabel": "high"})

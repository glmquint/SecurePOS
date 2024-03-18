

import time
from asyncio import wait
from random import randint

from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server



sender = JSONSender("../DataObjects/Schema/ElasticitySample.json", "http://127.0.0.1:5001/MessaginSystem")
sender.send('')
#sender2 = JSONSender("../DataObjects/Schema/AttackRiskLabelSchema.json", "http://127.0.0.1:5002/security_expert_endpoint")
#for x in range(0,50):
    #print(x)
#    y = randint(1,2)
#    x = randint(1,20)
#    if y == 1:
#        st = "High"
#    elif y == 2:
#        st = "Medium"
#    elif y == 3:
#        st = "Low"
#    st2 = st
#    if x == 10:
#        st2 = "High"
#    elif x == 2:
#        st2 = "Medium"
#    elif x == 3:
#        st2 = "Low"
#    sender2.send({"attackRiskLabel": st2})
#    sender.send({"attackRiskLabel": st})
#time.sleep(1)
#exit()
#sender2.send({"attackRiskLabel": "medium"})
#sender.send({"attackRiskLabel": "low"})
#
#sender.send({"attackRiskLabel": "low"})
#sender2.send({"attackRiskLabel": "high"})
#sender2.send({"attackRiskLabel": "medium"})
#sender.send({"attackRiskLabel": "low"})
#
##sender.send({"attackRiskLabel": "low"})
#sender2.send({"attackRiskLabel": "high"})
#
##
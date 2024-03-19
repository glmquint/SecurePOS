import time
from asyncio import wait
from random import randint

from src.DataObjects.Record import Label
from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server


var = Label(label="high")
sender2 = JSONSender("../DataObjects/Schema/Label.json", "http://127.0.0.1:5002/security_expert_endpoint")
sender = JSONSender("../DataObjects/Schema/Label.json", "http://127.0.0.1:5002/label_endpoint")
#sender.send(Label(label="high"))
sender.send(var.to_json())
for x in range(0,49):
    #print(x)
    y = randint(1,2)
    x = randint(1,20)
    if y == 1:
        st = "high"
    elif y == 2:
        st = "moderate"
    elif y == 3:
        st = "normal"
    st2 = st
    if x == 10:
        st2 = "high"
    elif x == 2:
        st2 = "moderate"
    elif x == 3:
        st2 = "normal"
    sender.send(var.to_json())
    sender2.send(var.to_json())
    #sender2.send({"label": st2})
    #sender.send({"label": st})
time.sleep(1)
exit()
sender2.send({"attackRiskLabel": "moderate"})
sender.send({"attackRiskLabel": "normal"})

sender.send({"attackRiskLabel": "normal"})
sender2.send({"attackRiskLabel": "high"})
sender2.send({"attackRiskLabel": "moderate"})
sender.send({"attackRiskLabel": "normal"})

sender.send({"attackRiskLabel": "normal"})
sender2.send({"attackRiskLabel": "high"})

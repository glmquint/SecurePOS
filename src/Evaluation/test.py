import time
import uuid
from asyncio import wait
from random import randint

from src.DataObjects.Record import Label, Record
from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server


#var = Label(label="high",uuid="bau")
sender2 = JSONSender("../DataObjects/Schema/Label.json", "http://127.0.0.1:5002/security_expert_endpoint")
sender = JSONSender("../DataObjects/Schema/Label.json", "http://127.0.0.1:5002/label_endpoint")
#sender.send(Label(label="high"))
#sender.send(var.to_json())
for x in range(50):
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
    uid=str(uuid.uuid4())
    sender.send(Label(label=st,uuid = uid))
    if randint(0,1000) < 10:
        print(uid)
        uid = str(uuid.uuid4())
        print(uid)
    sender2.send(Label(label=st2,uuid = uid))
    #sender2.send({"label": st2})
    #sender.send({"label": st})
#sender.send(Label(label="bau",uuid="ci"))
#sender2.send(Label(label="bau",uuid="cip"))
exit()
sender2.send({"attackRiskLabel": "moderate"})
sender.send({"attackRiskLabel": "normal"})

sender.send({"attackRiskLabel": "normal"})
sender2.send({"attackRiskLabel": "high"})
sender2.send({"attackRiskLabel": "moderate"})
sender.send({"attackRiskLabel": "normal"})

sender.send({"attackRiskLabel": "normal"})
sender2.send({"attackRiskLabel": "high"})

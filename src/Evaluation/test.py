import time
import uuid
from asyncio import wait
from random import randint, random

from src.DataObjects.Record import Label, Record
from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server


#var = Label(label="high",uuid="bau")
sender2 = JSONSender("../DataObjects/Schema/Label.json", "http://127.0.0.1:5002/security_expert_endpoint")
sender = JSONSender("../DataObjects/Schema/Label.json", "http://127.0.0.1:5002/label_endpoint")
#sender.send(Label(label="high"))
#sender.send(var.to_json())
a=[]
b=[]
ran = False
for x in range(50):
    y = randint(1,3)
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
    #sender.send(Label(label=st,uuid = uid))
    a.append(Label(label=st,uuid=uid))
    if randint(0,1000) < 10:
        print(uid)
        uid = str(uuid.uuid4())
        print(uid)
        ran = True
    b.append(Label(label=st2,uuid=uid))
sorted(a, key=lambda x: randint(0,50))
sorted(b, key=lambda x: randint(0,50))
inva = 50
invb = 50
for x in range(100):
    print(x)
    if inva == 0 and invb != 0:
        sender2.send(b[invb-1])
        inva = inva-1
        print("b:"+str(invb))
        continue
    if invb == 0 and inva != 0:
        sender.send(a[inva-1])
        inva = inva-1
        print("a:"+str(inva))
        continue
    if randint(0,10) < 5 and inva != 0:
        sender.send(a[inva-1])
        inva = inva - 1
        print("a:"+str(inva))
        continue
    elif invb != 0:
        sender2.send(b[invb-1])
        invb = invb - 1
        print("b:"+str(invb))
    else:
        sender.send(a[inva-a])
        inva = inva - 1
        print("a:"+str(inva))
    #sender2.send()
    #sender.send()
#sender2.send(Label(label=st2,uuid = uid))
    #sender2.send({"label": st2})
    #sender.send({"label": st})
#sender.send(Label(label="bau",uuid="ci"))
#sender2.send(Label(label="bau",uuid="cip"))
if ran:
    print("random!")
exit()
sender2.send({"attackRiskLabel": "moderate"})
sender.send({"attackRiskLabel": "normal"})

sender.send({"attackRiskLabel": "normal"})
sender2.send({"attackRiskLabel": "high"})
sender2.send({"attackRiskLabel": "moderate"})
sender.send({"attackRiskLabel": "normal"})

sender.send({"attackRiskLabel": "normal"})
sender2.send({"attackRiskLabel": "high"})

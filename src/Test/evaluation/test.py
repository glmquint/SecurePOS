"""simple test for the orchestrator"""
import os
import uuid
from random import randint, random

from src.DataObjects.Record import Label, Record
from src.JsonIO.JSONSender import JSONSender


sender2 = JSONSender(
    f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json",
    "http://127.0.0.1:5004/evaluation_security_label")
sender = JSONSender(
    f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json",
    "http://127.0.0.1:5004/evaluation_label")
a = []
b = []
uid = str(uuid.uuid4())
sender2.send(Label(label="low", uuid=uid))
sender.send(Label(label="high", uuid=uid))
uid = str(uuid.uuid4())
sender2.send(Label(label="low", uuid=uid))
sender.send(Label(label="low", uuid=uid))
uid = str(uuid.uuid4())
sender.send(Label(label="moderate", uuid=uid))
sender2.send(Label(label="high", uuid=uid))

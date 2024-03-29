"""simple system sender tester"""
from datetime import time

from src.Evaluation.EvaluationSystemSender import EvaluationSystemSender
from src.util import Message

s = EvaluationSystemSender()
message = "Test messaging at:" + time.now()
s.sendtomessaging(Message(msg=message))

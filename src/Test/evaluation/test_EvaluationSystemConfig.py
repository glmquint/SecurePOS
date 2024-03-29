"""simple test for the system config"""
from src.Evaluation.EvaluationSystemConfig import EvaluationSystemConfig

conf = EvaluationSystemConfig()
conf.load()
conf.write_state(0)
conf.load()
print(conf.tollerated_error)
print(conf.messaging_ip)

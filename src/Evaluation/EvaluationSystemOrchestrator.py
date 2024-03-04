import time

from src.Evaluation.EvaluationSystemConfig import EvaluationSystemConfig
from src.Evaluation.EvaluationSystemSender import EvaluationSystemSender
from src.Evaluation.LabelReceiver import LabelReceiver


class EvaluationSystemOrchestrator:
    def __init__(self):
        self.label_counter = 0
        self.simulateHumanTasks = False
        self.config = EvaluationSystemConfig()
        self.sender = EvaluationSystemSender()
        self.receiver = LabelReceiver()

    def isnumberoflabelssufficient(self):
        return self.label_counter >= 5000

    def run(self):
        print("start")
        self.receiver.receive()
        time.sleep(5)
        res = self.receiver.mbus.popTopic("label")
        time.sleep(5)
        while res != "empty":
            print(f"ricevuto:{res}")
            res = self.receiver.mbus.popTopic("label")
        return

    def main(self):
        self.run()
        return


if __name__ == "__main__":
    EvaluationSystemOrchestrator().main()

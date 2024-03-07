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
        return self.label_counter >= self.config.sufficient_label_number

    def run(self):
        print("start")
        self.receiver.receive()
        while not self.isnumberoflabelssufficient():
            res = self.receiver.mbus.popTopic("label")
            self.label_counter = self.label_counter + 1
            print(self.label_counter)
        print("Evaluation done.")
        return

    def main(self):
        self.run()
        return


if __name__ == "__main__":
    EvaluationSystemOrchestrator().main()

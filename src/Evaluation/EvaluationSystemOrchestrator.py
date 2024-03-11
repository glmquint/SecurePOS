import time

from src.Evaluation.EvaluationReportController import EvaluationReportController
from src.Evaluation.EvaluationSystemConfig import EvaluationSystemConfig
from src.Evaluation.EvaluationSystemSender import EvaluationSystemSender
from src.Evaluation.LabelReceiver import LabelReceiver


class EvaluationSystemOrchestrator:
    def __init__(self):
        self.label_counter = 0
        self.security_label_counter = 0
        self.simulateHumanTasks = False
        self.config = EvaluationSystemConfig()
        self.sender = EvaluationSystemSender()
        self.receiver = LabelReceiver()
        self.evaluation = EvaluationReportController()

    def isnumberoflabelssufficient(self):
        return self.label_counter >= self.config.sufficient_label_number \
               and self.security_label_counter >= self.config.sufficient_label_number

    def run(self):
        print("start")
        self.receiver.receive()
        while not self.isnumberoflabelssufficient():
            self.receiver.mbus.popTopic("label")
            self.label_counter = self.label_counter + 1
            self.receiver.mbus.popTopic("sec_label")
            self.security_label_counter = self.security_label_counter + 1
        self.evaluation.update()
        print("Development phase done.")
        return

    def main(self):
        self.config.load()
        if self.config.state == 0:
            self.run()
            self.config.write_state(1)
            if self.config.simulate_human_task:
                self.evaluation.getresult(True)
                self.config.write_state(0)
        else:
            self.evaluation.getresult()
            self.config.write_state(0)
        return


if __name__ == "__main__":
    EvaluationSystemOrchestrator().main()

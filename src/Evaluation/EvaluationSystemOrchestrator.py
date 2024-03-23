import time


from src.Evaluation.EvaluationReportController import EvaluationReportController
from src.Evaluation.EvaluationSystemConfig import EvaluationSystemConfig
from src.Evaluation.EvaluationSystemSender import EvaluationSystemSender
from src.Evaluation.LabelReceiver import LabelReceiver
from src.util import log


class EvaluationSystemOrchestrator:
    def __init__(self):
        self.label_counter = 0
        self.security_label_counter = 0
        self.simulateHumanTasks = False
        self.config = EvaluationSystemConfig()
        self.sender = EvaluationSystemSender()
        self.receiver = LabelReceiver(self.config.port)
        self.evaluation = EvaluationReportController(self.config)

    def isnumberoflabelssufficient(self):
        return self.label_counter >= self.config.sufficient_label_number \
               and self.security_label_counter >= self.config.sufficient_label_number

    def run(self):
        print("start")
        while not self.isnumberoflabelssufficient(): # TODO @mirco: retrieve n and delete n from db as check if we have enough labels
            self.receiver.mbus.popTopic("label")
            self.label_counter = self.label_counter + 1
            self.receiver.mbus.popTopic("sec_label")
            self.security_label_counter = self.security_label_counter + 1
        self.evaluation.update()
        self.label_counter = 0
        self.security_label_counter = 0
        print("Development phase done.")
        return

    def main(self):
        self.config.load()
        self.receiver.receive()
        #while True:
        #self.config.load()
        print("=====================================")
        while True:
            if self.config.state == 0:
                self.run()
                self.config.write_state(1)
                if self.config.simulate_human_task:
                    self.evaluation.getresult(True)
                    self.config.write_state(0)
                else:
                    return
            else:
                self.evaluation.getresult()
                self.config.write_state(0)
        return


if __name__ == "__main__":
        EvaluationSystemOrchestrator().main()

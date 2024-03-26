import time


from src.Evaluation.EvaluationReportController import EvaluationReportController
from src.Evaluation.EvaluationSystemConfig import EvaluationSystemConfig
from src.Evaluation.EvaluationSystemSender import EvaluationSystemSender
from src.Evaluation.LabelReceiver import LabelReceiver
from src.util import log, Message


class EvaluationSystemOrchestrator:
    def __init__(self, config: EvaluationSystemConfig = None):
        self.label_counter = 0
        self.security_label_counter = 0
        self.simulateHumanTasks = False
        if not config:
            config = EvaluationSystemConfig()
        self.config = config
        self.sender = EvaluationSystemSender()
        self.receiver = LabelReceiver(self.config.port)
        self.evaluation = EvaluationReportController(self.config)
        self.sender = EvaluationSystemSender()

    def isnumberoflabelssufficient(self):
        return self.label_counter >= self.config.sufficient_label_number \
               and self.security_label_counter >= self.config.sufficient_label_number

    def run(self):
        print("start")
        while not self.isnumberoflabelssufficient():
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
                try:
                    self.run()
                except Exception as e:
                    print(e)
                    continue
                self.config.write_state(1)
                if self.config.simulate_human_task:
                    self.evaluation.getresult(True)
                    self.config.write_state(0)
                else:
                    return
            else:
                self.evaluation.getresult()
                self.sender.sendtomessaging(Message(msg="Evaluation complete."))
                self.config.write_state(0)
        return


if __name__ == "__main__":
        EvaluationSystemOrchestrator().main()

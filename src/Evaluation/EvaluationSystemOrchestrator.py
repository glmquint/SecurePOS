from src.Evaluation.EvaluationReportController import EvaluationReportController
from src.Evaluation.EvaluationSystemConfig import EvaluationSystemConfig
from src.Evaluation.EvaluationSystemSender import EvaluationSystemSender
from src.Evaluation.LabelReceiver import LabelReceiver
from src.util import Message


class EvaluationSystemOrchestrator:
    """
        This class is responsible for orchestrating the evaluation system. It initializes the system with a configuration,
        manages the label counters, and controls the main loop of the system.

        Attributes:
            label_counter: A counter for the labels.
            security_label_counter: A counter for the security labels.
            simulate_human_task: A boolean value that indicates whether to simulate a human task.
            config: An object of EvaluationSystemConfig that handles the configuration of the system.
            sender: An object of EvaluationSystemSender that handles the sending of messages.
            receiver: An object of LabelReceiver that handles the receiving of labels.
            evaluation: An object of EvaluationReportController that handles the evaluation report.

        Methods:
            isnumberoflabelssufficient: Checks if the number of labels is sufficient.
            run: Runs the main loop of the system.
            main: The main function of the system.
    """
    def __init__(self, config: EvaluationSystemConfig = None):
        self.label_counter = 0
        self.security_label_counter = 0
        self.simulate_human_task = False
        if not config:
            config = EvaluationSystemConfig()
        self.config = config
        self.sender = EvaluationSystemSender(self.config)
        self.receiver = LabelReceiver(self.config.port)
        self.evaluation = EvaluationReportController(self.config)

    def isnumberoflabelssufficient(self):
        """"check if labels are sufficient"""
        return self.label_counter >= self.config.sufficient_label_number \
            and self.security_label_counter >= self.config.sufficient_label_number

    def run(self):
        """running function"""
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

    def main(self):
        """main function"""
        self.config.load()
        self.receiver.receive()
        print("=====================================")
        while True:
            if self.config.state == 0:
                try:
                    self.run()
                except Exception as exc:
                    print(exc)
                    continue
                self.config.write_state(1)
                if self.config.simulate_human_task:
                    self.evaluation.getresult(True)
                    self.config.write_state(0)
                else:
                    return
            else:
                self.evaluation.getresult()
                self.sender.sendtomessaging(
                    Message(msg="Evaluation complete."))
                self.config.write_state(0)
        return


if __name__ == "__main__":
    EvaluationSystemOrchestrator().main()

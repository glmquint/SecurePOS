from src.Evaluation.EvaluationSystemConfig import EvaluationSystemConfig
from src.Evaluation.EvaluationSystemSender import EvaluationSystemSender
from src.Evaluation.LabelReceiver import LabelReceiver


class EvaluationSystemOrchestrator:
    def __init__(self):
        label_counter = 0
        simulateHumanTasks = False
        config = EvaluationSystemConfig()
        sender = EvaluationSystemSender()
        receiver = LabelReceiver()

    def isnumberoflabelssufficient(self):
        return self.label_counter >= 5000

    def run(self):
        return

    def main(self):
        self.run()
        return

    if __name__ == "__main__":
        main()

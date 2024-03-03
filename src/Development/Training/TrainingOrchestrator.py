from src.Development.LearningSetReceiver import LearningSetReceiver
from src.Development.ReportController import ReportController
from src.Development.Training.TrainProcess import TrainProcess
from src.MessageBus.MessageBus import MessageBus


class TrainingOrchestrator:
    message_bus: MessageBus = None
    train_process: TrainProcess = None
    report_controller: ReportController = None
    number_of_iterations: int = 0
    learning_set: LearningSet = None
    is_ongoing_validation: bool = False
    number_of_iter_is_fine: bool = False

    def __init__(self, report_controller: ReportController, message_bus: MessageBus):
        self.train_process = TrainProcess()
        self.message_bus = message_bus
        self.report_controller = report_controller

    def check_learning_plot(self):
        input("> learning plot created! Please insert the decision in learning_result.txt file")
        with open('learning_result.txt', 'r') as file:
            return "Yes" == file.read()

    def start(self) -> bool:
        self.learning_set = self.message_bus.popTopic("LearningSet")
        self.train_process.set_average_hyperparameters()
        self.train_process.set_number_of_iterations(0)  # dummy argument
        while self.is_ongoing_validation:
            self.train_process.train()
            if not self.is_ongoing_validation:
                self.report_controller.create_learning_plot()
                self.number_of_iter_is_fine = self.check_learning_plot()
                if not self.number_of_iter_is_fine:
                    return True
            # increment hyperparam in grid search
        return False

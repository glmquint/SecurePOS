from src.Development.LearningSetReceiver import LearningSetReceiver
from src.Development.ReportController import ReportController
from src.Development.Training.TrainProcess import TrainProcess
from src.MessageBus.MessageBus import MessageBus


class TrainingOrchestrator:
    learning_receiver : LearningSetReceiver = None
    message_bus : MessageBus = None
    train_process : TrainProcess = None
    report_controller : ReportController = None

    def __init__(self):
        self.train_process = TrainProcess()
        self.message_bus = MessageBus()
        self.learning_receiver = LearningSetReceiver(self.message_bus)
        self.report_controller = ReportController()



from src.Development.DevSystemStatus import DevSystemStatus
from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemSender import DevelopmentSystemSender
from src.Development.LearningSetReceiver import LearningSetReceiver
from src.Development.ReportController import ReportController
from src.Development.Testing.TestingOrchestrator import TestingOrchestrator
from src.Development.Training.TrainingOrchestrator import TrainingOrchestrator
from src.Development.Validation.ValidationOrchestrator import ValidationOrchestrator
from src.MessageBus.MessageBus import MessageBus
from threading import Thread


class DevelopmentSystemMasterOrchestrator:
    simulate_humane_task: bool
    train_orchestrator: TrainingOrchestrator = None
    validation_orchestrator: ValidationOrchestrator = None
    test_orchestrator: TestingOrchestrator = None
    development_system_sender: DevelopmentSystemSender = None
    development_system_configurations: DevelopmentSystemConfigurations = None
    learning_set_receiver: LearningSetReceiver = None
    message_bus: MessageBus = None
    report_controller: ReportController = None
    status: DevSystemStatus = None

    def __init__(self, simulate_humane_task: bool):
        self.status = DevSystemStatus("status.json")
        self.status.load_status()
        self.development_system_configurations = DevelopmentSystemConfigurations()
        self.message_bus = MessageBus(["LearningSet", "Classifier"])
        self.report_controller = ReportController()
        self.simulate_humane_task = simulate_humane_task
        self.train_orchestrator = TrainingOrchestrator(self.status, self.report_controller, self.message_bus,
                                                       self.development_system_configurations.hyperparameters)
        self.validation_orchestrator = ValidationOrchestrator(self.status, self.report_controller, self.message_bus)
        self.test_orchestrator = TestingOrchestrator(self.status, self.report_controller, self.message_bus)
        self.learning_set_receiver = LearningSetReceiver(self.message_bus)

    def start(self):
        while True:
            if self.status.status == "receive_learning_set":
                th = Thread(target=self.learning_set_receiver.run)
                th.start()
                self.status.save_status("set_avg_hyperparam", False)
            elif self.status.status in ["set_avg_hyperparam", "set_number_of_iterations", "train", "check_validation",
                                        "generate_learning_plot", "check_learning_plot", "check_number_of_iterations"]:
                self.train_orchestrator.start()
            elif self.status.status in ["set_hyperparam", "check_ongoing_validation", "generate_validation_report",
                                        "check_validation_report", "check_valid_classifier"]:
                self.validation_orchestrator.start()
            elif self.status.status in ["generate_test_report", "check_test_report"]:
                self.test_orchestrator.start()
            elif self.status.status == "send_config":
                self.development_system_sender.send_to_messaging(self.test_orchestrator.config)
            elif self.status.status == "send_classifier":
                self.development_system_sender.send_to_production(self.test_orchestrator.classifier)
            else:
                raise Exception("Invalid status")

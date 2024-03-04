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

    def __init__(self, simulate_humane_task: bool):
        self.development_system_configurations = DevelopmentSystemConfigurations()
        self.message_bus = MessageBus(["LearningSet", "Classifier"])
        self.report_controller = ReportController()
        self.simulate_humane_task = simulate_humane_task
        self.train_orchestrator = TrainingOrchestrator(self.report_controller,self.message_bus,self.development_system_configurations.hyperparameters)
        self.validation_orchestrator = ValidationOrchestrator(self.report_controller, self.message_bus)
        self.test_orchestrator = TestingOrchestrator(self.report_controller, self.message_bus)
        self.learning_set_receiver = LearningSetReceiver(self.message_bus)

    def start(self):
        th = Thread(target=self.learning_set_receiver.run)
        th.start()
        not_sufficient_number_of_iterations = True
        not_valid_classifier = True
        test_passed = False
        while not_valid_classifier:
            while not_sufficient_number_of_iterations:
                not_sufficient_number_of_iterations = self.train_orchestrator.start()
            not_valid_classifier = self.validation_orchestrator.start()
        test_passed = self.test_orchestrator.start()
        if test_passed:
            pass
            # self.development_system_sender.send_to_production(self.test_orchestrator.classifier)
        else:
            pass
            # self.development_system_sender.send_to_messaging(self.test_orchestrator.configuration)

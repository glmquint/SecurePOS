from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
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
    status: DevelopmentSystemStatus = None

    def __init__(self, simulate_humane_task: bool):
        self.status = DevelopmentSystemStatus("development_system_status.json", "schema/status_schema.json")
        self.status.load_status()
        self.simulate_humane_task = simulate_humane_task
        self.development_system_configurations = DevelopmentSystemConfigurations('schema/config_schema.json')
        self.development_system_configurations.load_config('config/config.json', True)
        self.message_bus = MessageBus(self.development_system_configurations.topics)
        self.report_controller = ReportController(self.message_bus)
        self.train_orchestrator = TrainingOrchestrator(self.status, self.report_controller, self.message_bus,
                                                       self.development_system_configurations)
        self.validation_orchestrator = ValidationOrchestrator(self.status, self.report_controller, self.message_bus,
                                                              self.development_system_configurations)
        self.test_orchestrator = TestingOrchestrator(self.status, self.report_controller, self.message_bus)
        self.learning_set_receiver = LearningSetReceiver(self.message_bus)
        self.development_system_sender = DevelopmentSystemSender(
            self.development_system_configurations.messaging_system_receiver,
            self.development_system_configurations.production_system_receiver)

    def start(self):
        while True:
            if self.status.status == "receive_learning_set":
                th = Thread(target=self.learning_set_receiver.run)
                th.start()
                self.status.status = "pop_learning_set"
            elif self.status.status in ["pop_learning_set", "set_avg_hyperparams", "set_number_of_iterations", "train",
                                        "check_learning_plot"]:
                self.train_orchestrator.start()
            elif self.status.status in ["set_hyperparams", "do_grid_search",
                                        "generate_validation_report",
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


dsmo = DevelopmentSystemMasterOrchestrator(False)
print("Starting Development System Master Orchestrator...")
dsmo.start()

import os.path
from threading import Thread
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemSender import DevelopmentSystemSender
from src.Development.LearningSetReceiver import LearningSetReceiver
from src.Development.ReportController import ReportController
from src.Development.Testing.TestingOrchestrator import TestingOrchestrator
from src.Development.Training.TrainingOrchestrator import TrainingOrchestrator
from src.Development.Validation.ValidationOrchestrator import ValidationOrchestrator
from src.MessageBus.MessageBus import MessageBus


class DevelopmentSystemMasterOrchestrator:
    """
    A class used to orchestrate the operations of the development system.

    Attributes
    ----------
    train_orchestrator : TrainingOrchestrator
        The orchestrator for the training process.
    validation_orchestrator : ValidationOrchestrator
        The orchestrator for the validation process.
    test_orchestrator : TestingOrchestrator
        The orchestrator for the testing process.
    development_system_sender : DevelopmentSystemSender
        The sender for the development system.
    development_system_configurations : DevelopmentSystemConfigurations
        The configurations for the development system.
    learning_set_receiver : LearningSetReceiver
        The receiver for the learning set.
    message_bus : MessageBus
        The message bus for the system.
    report_controller : ReportController
        The controller for the reports.
    status : DevelopmentSystemStatus
        The status of the development system.

    Methods
    -------
    __init__(self, status: DevelopmentSystemStatus = None, config: DevelopmentSystemConfigurations = None)
        Initializes the DevelopmentSystemMasterOrchestrator class.
    start(self)
        Starts the orchestrator and manages the operations based on the system status.
    """
    # class implementation...
    train_orchestrator: TrainingOrchestrator = None
    validation_orchestrator: ValidationOrchestrator = None
    test_orchestrator: TestingOrchestrator = None
    development_system_sender: DevelopmentSystemSender = None
    development_system_configurations: DevelopmentSystemConfigurations = None
    learning_set_receiver: LearningSetReceiver = None
    message_bus: MessageBus = None
    report_controller: ReportController = None
    status: DevelopmentSystemStatus = None

    def __init__(self, status: DevelopmentSystemStatus = None,
                 config: DevelopmentSystemConfigurations = None):
        if status is None:
            self.status = DevelopmentSystemStatus(
                f"{os.path.dirname(__file__)}/development_system_status.json",
                f"{os.path.dirname(__file__)}/schema/status_schema.json")
            self.status.load_status()
        else:
            self.status = status
        if config is None:
            config = DevelopmentSystemConfigurations(
                f'{os.path.dirname(__file__)}/schema/config_schema.json')
        self.development_system_configurations = config
        self.development_system_configurations.load_config(
            f'{os.path.dirname(__file__)}/config/config.json',
            True)
        self.message_bus = MessageBus(
            self.development_system_configurations.topics)
        self.report_controller = ReportController(self.message_bus)
        self.train_orchestrator = TrainingOrchestrator(
            self.status,
            self.report_controller,
            self.message_bus,
            self.development_system_configurations)
        self.validation_orchestrator = ValidationOrchestrator(
            self.status,
            self.report_controller,
            self.message_bus,
            self.development_system_configurations)
        self.test_orchestrator = TestingOrchestrator(
            self.status,
            self.report_controller,
            self.message_bus,
            self.development_system_configurations)
        self.learning_set_receiver = LearningSetReceiver(
            self.message_bus, self.development_system_configurations.endpoint_url)
        self.development_system_sender = DevelopmentSystemSender(
            self.development_system_configurations, self.status)

    def start(self):
        while True:
            if self.status.status == "receive_learning_set":
                th = Thread(target=self.learning_set_receiver.run, kwargs={
                            'port': self.development_system_configurations.port})
                th.daemon = True
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
                self.development_system_sender.send_to_messaging()
                break
            elif self.status.status == "send_classifier":
                self.development_system_sender.send_to_production()
                break
            else:
                raise Exception("Invalid status")


if __name__ == "__main__":
    dsmo = DevelopmentSystemMasterOrchestrator()
    print("Starting Development System Master Orchestrator...")
    dsmo.start()

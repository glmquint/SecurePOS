from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemSender import DevelopmentSystemSender
from src.Development.Testing import TestingOrchestrator
from src.Development.Training.TrainingOrchestrator import TrainingOrchestrator
from src.Development.Validation import ValidationOrchestrator


class DevelopmentSystemMasterOrchestrator:
    simulate_humane_task: bool
    train_orchestrator: TrainingOrchestrator = None
    validation_orchestrator: ValidationOrchestrator = None
    test_orchestrator: TestingOrchestrator = None
    development_system_sender: DevelopmentSystemSender = None
    development_system_configurations: DevelopmentSystemConfigurations = None

    def __init__(self, simulate_humane_task: bool):
        self.simulate_humane_task = simulate_humane_task

    def run(self):
        pass

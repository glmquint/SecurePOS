import json

from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.ReportController import ReportController
from src.Development.Training.HyperParameterLimit import HyperParameterLimit
from src.Development.Training.TrainProcess import TrainProcess, LearningSet
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController


class TrainingOrchestrator:
    message_bus: MessageBus = None
    train_process: TrainProcess = None
    report_controller: ReportController = None
    number_of_iterations: int = 0
    learning_set: LearningSet = None
    is_ongoing_validation: bool = False
    number_of_iter_is_fine: bool = False
    storage_controller: StorageController = None
    status: DevelopmentSystemStatus = None
    hyperparameters: HyperParameterLimit = None

    def __init__(self, status: DevelopmentSystemStatus, report_controller: ReportController, message_bus: MessageBus,
                 hyperparameters: HyperParameterLimit):
        self.message_bus = message_bus
        self.report_controller = report_controller
        self.status = status
        self.hyperparameters = hyperparameters
        self.train_process = TrainProcess(self.status, self.message_bus, self.hyperparameters)

    def get_AI_export_response(self) -> int:
        ret_val = -1
        with open('learning_result.json', 'r') as json_file:  # validate learning_result.json
            ret_val = 0
            data = json.load(json_file)
            if data['result'] in ["ok", "OK", "Ok"]:
                ret_val = 1
        return ret_val

    def start(self):
        while True:
            if self.status.status in ["receive_learning_set", "set_avg_hyperparams", "set_number_of_iterations",
                                      "train"]:
                self.train_process.start()
            if not self.status.should_validate:
                self.report_controller.create_learning_plot()
                self.status.status = "check_learning_plot"
                self.status.save_status()
                break
            elif self.status.status == "check_learning_plot":
                response = self.get_AI_export_response()
                if response == 0:
                    self.status.status = "set_number_of_iterations"
                elif response == 1:
                    self.status.status = "set_hyperparam"
                self.status.save_status()
                break
            else:
                raise Exception("Invalid status")

import json
import random

from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.ReportController import ReportController
from src.Development.Training.HyperParameterLimit import HyperParameterLimit
from src.Development.Training.TrainProcess import TrainProcess
from src.JsonIO.JsonValidator import JSONValidator
from src.MessageBus.MessageBus import MessageBus


class TrainingOrchestrator:
    message_bus: MessageBus = None
    train_process: TrainProcess = None
    report_controller: ReportController = None
    status: DevelopmentSystemStatus = None
    hyperparameters: HyperParameterLimit = None
    configurations: DevelopmentSystemConfigurations = None

    def __init__(self, status: DevelopmentSystemStatus, report_controller: ReportController, message_bus: MessageBus,
                 configurations: DevelopmentSystemConfigurations):
        self.message_bus = message_bus
        self.report_controller = report_controller
        self.status = status
        self.hyperparameters = configurations.hyperparameters
        self.train_process = TrainProcess(self.status, self.message_bus, configurations)
        self.configurations = configurations

    def get_ai_export_response(self) -> int:
        print(f'[{self.__class__.__name__}]: getting AI expert response')
        ret_val = -1
        try:
            with open('Training/learning_result.json', 'r') as json_file:
                ret_val = 0
                data = json.load(json_file)
                JSONValidator("schema/result_schema.json").validate_data(data)
                if data['result'] in [""]:
                    ret_val = -1  # AI expert has not filled the file
                elif data['result'] in ["ok", "OK", "Ok", "oK"]:
                    ret_val = 1
                    print(f'[{self.__class__.__name__}]: learning phase is ok')
        except FileNotFoundError as e:  # create file so that AI expert can fill it
            print('File learning_result.json not found, creating it...')
            with open('Training/learning_result.json', 'w') as json_file:
                print("Please insert your decision in learning_result.json")
                json.dump({"result": ""}, json_file)
        finally:
            return ret_val

    def start(self):
        while True:
            if self.status.status == "pop_learning_set":
                self.train_process.receive_learning_set()
                self.status.status = "set_avg_hyperparams"
            elif self.status.status == "set_avg_hyperparams":
                self.train_process.set_average_hyperparameters()
                self.status.status = "set_number_of_iterations"
            elif self.status.status == "set_number_of_iterations":
                if self.configurations.stop_and_go:
                    number_of_iterations = self.train_process.get_number_of_iterations()
                else:  # stop & go is simulated
                    number_of_iterations = random.randint(10, 50)
                if number_of_iterations > 0:
                    self.status.number_of_iterations = number_of_iterations
                    self.status.status = "train"
                else:
                    print("Please insert a number >0 for the number of iterations")
                    self.status.status = "set_number_of_iterations"
                    self.status.save_status()
            elif self.status.status == "train":
                self.train_process.train()
                if not self.status.should_validate:
                    print("Creating learning plot")
                    self.report_controller.create_learning_plot()
                    self.status.status = "check_learning_plot"
            elif self.status.status == "check_learning_plot":
                if self.configurations.stop_and_go:
                    response = self.get_ai_export_response()
                else:
                    response = random.randint(0, 1)
                if response < 0:
                    self.status.save_status()
                elif response == 0:
                    self.status.status = "set_number_of_iterations"
                    self.train_process.remove_classifiers('classifiers')
                    self.train_process.remove_precedent_response('Training/learning_result')
                    self.train_process.remove_precedent_response('Training/number_of_iterations')
                    if self.configurations.stop_and_go:
                        self.status.save_status()
                    else:
                        break
                elif response == 1:
                    self.status.status = "set_hyperparams"
                break
            else:
                raise Exception("Invalid status")

import json

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from src.Development.Classifier import Classifier
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.Training.HyperParameterLimit import HyperParameterLimit
from src.JsonIO.JsonValidator import JSONValidator
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController


class LearningSet:
    pass


class TrainProcess:
    number_of_iterations: int = None
    classifier: Classifier = None
    grid_search: GridSearchCV = None
    hyperparameters: HyperParameterLimit = None
    avg_hyperparameters: dict = None
    status: DevelopmentSystemStatus = None
    learning_set: LearningSet = None

    def set_average_hyperparameters(self):
        self.avg_hyperparameters = {}
        for key in self.hyperparameters.__dict__:
            print(self.hyperparameters.__dict__[key])
            self.avg_hyperparameters[key] = (self.hyperparameters.__dict__[key]['min'] +
                                             self.hyperparameters.__dict__[key]['max']) / 2

    def get_number_of_iterations(self) -> int:
        ret_val = -1
        try:
            with open('Training/number_of_iterations.json', 'r') as json_file:
                data = json.load(json_file)
                JSONValidator("schema/iteration_schema.json").validate_data(data)
                ret_val = data['number_of_iterations']
        except FileNotFoundError as e:  # create file so that AI expert can fill it
            with open('Training/number_of_iterations.json', 'w') as json_file:
                json.dump({"number_of_iterations": 0}, json_file)
        finally:
            return ret_val

    def __init__(self, status: DevelopmentSystemStatus, message_bus: MessageBus, hyperparameters: HyperParameterLimit):
        self.status = status
        self.message_bus = message_bus
        self.hyperparameters = hyperparameters

    def train(self):
        pass

    def start(self):
        while True:
            if self.status.status == "receive_learning_set":
                self.learning_set = self.message_bus.popTopic("LearningSet")
                self.status.status = "set_avg_hyperparams"
            elif self.status.status == "set_avg_hyperparams":
                self.set_average_hyperparameters()
                self.status.status = "set_number_of_iterations"
            elif self.status.status == "set_number_of_iterations":
                self.number_of_iterations = self.get_number_of_iterations()
                if self.number_of_iterations > 0:
                    self.status.status = "train"
                else:
                    self.status.save_status()
            elif self.status.status == "train":
                self.train()
                self.status.status = "check_validation"
                break
            else:
                raise Exception("Invalid status")

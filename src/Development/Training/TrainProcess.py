import itertools
import json

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from src.Development.Classifier import Classifier
from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.Training.HyperParameterLimit import HyperParameterLimit
from src.Development.Training.LearningPlotModel import LearningPlotModel
from src.JsonIO.JsonValidator import JSONValidator
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController


class LearningSet:
    pass


class TrainProcess:
    number_of_iterations: int = None
    classifier: Classifier = None
    grid_search = None
    hyperparameters: HyperParameterLimit = None
    avg_hyperparameters: dict = None
    status: DevelopmentSystemStatus = None
    learning_set: LearningSet = None
    configurations: DevelopmentSystemConfigurations = None
    current_hyperparameter: tuple = None

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

    def __init__(self, status: DevelopmentSystemStatus, message_bus: MessageBus, hyperparameters: HyperParameterLimit,
                 configurations: DevelopmentSystemConfigurations):
        self.status = status
        self.message_bus = message_bus
        self.hyperparameters = hyperparameters
        self.configurations = configurations

    def train(self):
        if not self.status.should_validate:
            self.classifier = Classifier(self.avg_hyperparameters['number_of_neurons'],
                                         self.avg_hyperparameters['number_of_layers'])
        else:
            self.classifier = Classifier(self.current_hyperparameter[0],
                                         self.current_hyperparameter[1])
        self.classifier.model.fit(self.learning_set.X_train, self.learning_set.Y_train)
        if not self.status.should_validate:
            loss_curve = self.classifier.get_loss_curve()
            learning_plot_model = LearningPlotModel(loss_curve, self.number_of_iterations, self.loss_threshold)
            self.message_bus.pushTopic("learning_plot", learning_plot_model)
        else:  # TODO implement the validation part
            self.classifier.validation_error = 0.1

    def set_hyperparameters(self, next_hyperparam: tuple):
        self.current_hyperparameter = next_hyperparam

    def create_grid_search(self):
        layers = []
        for i in range(self.configurations.hyperparameters.number_of_layers['min'],
                       self.configurations.hyperparameters.number_of_layers['max'] + 1,
                       self.configurations.hyperparameters.number_of_layers['step']):
            layers.append(i)
        neurons = []
        for i in range(self.configurations.hyperparameters.number_of_neurons['min'],
                       self.configurations.hyperparameters.number_of_neurons['max'] + 1,
                       self.configurations.hyperparameters.number_of_neurons['step']):
            neurons.append(i)
        self.grid_search = list(itertools.product(layers, neurons))

    def perform_grid_search(self):
        for (number_of_layers, number_of_neurons) in self.grid_search:
            self.set_hyperparameters((number_of_layers, number_of_neurons))
            self.train()
            self.classifier.save_model('model/here')  # TODO change_path

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
                if not self.status.should_validate:
                    self.status.status = "check_learning_plot"
                break
            elif self.status.status == "do_grid_search":
                if not self.status.should_validate:
                    self.create_grid_search()
                    self.status.should_validate = True
                    self.perform_grid_search()
                    self.status.should_validate = False
                    # push the ValidationReport
            else:
                raise Exception("Invalid status")

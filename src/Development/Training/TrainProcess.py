import itertools
import json

from src.Development.Classifier import Classifier
from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.LearningSet import LearningSet
from src.Development.Training.HyperParameterLimit import HyperParameterLimit
from src.Development.Training.LearningPlotModel import LearningPlotModel
from src.JsonIO.JsonValidator import JSONValidator
from src.MessageBus.MessageBus import MessageBus


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
        for key in self.configurations.hyperparameters.__dict__:
            self.avg_hyperparameters[key] = (self.configurations.hyperparameters.__dict__[key]['min'] +
                                             self.configurations.hyperparameters.__dict__[key]['max']) / 2
        self.status.average_hyperparameters = self.avg_hyperparameters

    def receive_learning_set(self):
        self.learning_set = self.message_bus.popTopic("LearningSet")
        self.status.learning_set = self.learning_set

    def get_number_of_iterations(self) -> int:
        ret_val = -1
        try:
            with open('Training/number_of_iterations.json', 'r') as json_file:
                data = json.load(json_file)
                JSONValidator("schema/iteration_schema.json").validate_data(data)
                ret_val = data['number_of_iterations']
                self.number_of_iterations = ret_val
        except FileNotFoundError as e:  # create file so that AI expert can fill it
            with open('Training/number_of_iterations.json', 'w') as json_file:
                json.dump({"number_of_iterations": 0}, json_file)
        finally:
            return ret_val

    def __init__(self, status: DevelopmentSystemStatus, message_bus: MessageBus,
                 configurations: DevelopmentSystemConfigurations):
        self.status = status
        self.message_bus = message_bus
        self.configurations = configurations

    def train(self):
        if self.avg_hyperparameters is None and self.learning_set is None:  # if restarted load from file
            self.avg_hyperparameters = self.status.average_hyperparameters
            self.learning_set = self.status.learning_set
        if not self.status.should_validate:
            self.classifier = Classifier(self.avg_hyperparameters['number_of_neurons'],
                                         self.avg_hyperparameters['number_of_layers'], self.number_of_iterations)
        else:
            self.classifier = Classifier(self.current_hyperparameter[0],
                                         self.current_hyperparameter[1], self.number_of_iterations)
        self.classifier.model.fit(self.learning_set.trainingSet, self.learning_set.trainingSetLabel)
        if not self.status.should_validate:
            loss_curve = self.classifier.get_loss_curve()
            learning_plot_model = LearningPlotModel(loss_curve, self.number_of_iterations, self.configurations.loss_threshold)
            self.message_bus.pushTopic("learning_plot", learning_plot_model)
        else:  # TODO implement the validation part
            self.classifier.validation_error = 0.1

    def set_hyperparameters(self, next_hyperparam: tuple):
        self.current_hyperparameter = next_hyperparam

    def set_hyperparams(self):
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
            # TODO implement saving of the 5 best models


import itertools
import json
import pandas as pd
from sklearn.metrics import mean_squared_error, accuracy_score
from src.Development.Classifier import Classifier
from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.Development.LearningSet import LearningSet
from src.Development.Training.Scoreboard import Scoreboard
from src.Development.Training.HyperParameterLimit import HyperParameterLimit
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
    grid_space: Scoreboard = None

    def set_average_hyperparameters(self):
        self.avg_hyperparameters = {}
        for key in self.configurations.hyperparameters.__dict__:
            self.avg_hyperparameters[key] = (self.configurations.hyperparameters.__dict__[key]['min'] +
                                             self.configurations.hyperparameters.__dict__[key]['max']) // 2
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
        if self.status.learning_set is not None:
            self.learning_set = self.status.learning_set
        if self.status.number_of_iterations != -1:
            self.number_of_iterations = self.status.number_of_iterations
        if self.status.average_hyperparameters is not None:
            self.avg_hyperparameters = self.status.average_hyperparameters

    def train(self, current_iteration: int = 0):
        if not self.status.should_validate:
            self.classifier = Classifier(self.avg_hyperparameters['number_of_neurons'],
                                         self.avg_hyperparameters['number_of_layers'], self.number_of_iterations)
        else:
            self.classifier = Classifier(self.current_hyperparameter[0],
                                         self.current_hyperparameter[1], self.number_of_iterations,
                                         f'Classifier {current_iteration}')
        self.classifier.model.fit(self.learning_set.trainingSet, pd.Series(self.learning_set.trainingSetLabel))
        self.classifier.save_model('Training')  # TODO remove me
        if not self.status.should_validate:
            loss_curve = self.classifier.get_loss_curve()
            self.message_bus.pushTopic("learning_plot",
                                       [loss_curve, self.number_of_iterations, self.configurations.loss_threshold])

    def validate(self):
        y_train_pred = self.classifier.model.predict(self.learning_set.trainingSet)
        y_val_predicted = self.classifier.model.predict(self.learning_set.validationSet)
        # TODO: maybe change to minimum
        mse = self.classifier.model.best_loss_
        train_error = 1.0 - accuracy_score(self.learning_set.trainingSetLabel, y_train_pred)
        val_error = 1.0 - accuracy_score(self.learning_set.validationSetLabel, y_val_predicted)
        self.grid_space.insert_classifier(self.classifier, mse, train_error, val_error)

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
        iteration = 0
        self.grid_space = Scoreboard(self.configurations.classifiers_limit)
        for (number_of_layers, number_of_neurons) in self.grid_search:
            iteration = iteration + 1
            self.set_hyperparameters((number_of_layers, number_of_neurons))
            self.train(iteration)
            self.validate()
        # grid search is finished, push the scoreboard in order to obtain validation report
        self.message_bus.pushTopic("Scoreboard", self.grid_space)

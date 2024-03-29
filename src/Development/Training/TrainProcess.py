import itertools
import json
import math
import os

import pandas as pd
from sklearn.metrics import accuracy_score, mean_squared_error

from src.DataObjects.Classifier import Classifier
from src.Development.DevelopmentSystemConfigurations import DevelopmentSystemConfigurations
from src.Development.DevelopmentSystemStatus import DevelopmentSystemStatus
from src.DataObjects.LearningSet import LearningSet
from src.Development.Training.Scoreboard import Scoreboard
from src.Development.Training.HyperParameterLimit import HyperParameterLimit
from src.JsonIO.JsonValidator import JSONValidator
from src.MessageBus.MessageBus import MessageBus


class TrainProcess:
    """
    A class used to manage the training process in the development system.

    Attributes
    ----------
    number_of_iterations : int
        The number of iterations for the training process.
    classifier : Classifier
        The classifier being trained.
    grid_search : list
        The list of hyperparameters to be used in the grid search.
    hyperparameters : HyperParameterLimit
        The limits for the hyperparameters used in the training process.
    avg_hyperparameters : dict
        The average values of the hyperparameters.
    status : DevelopmentSystemStatus
        The current status of the development system.
    learning_set : LearningSet
        The learning set used in the training process.
    configurations : DevelopmentSystemConfigurations
        The configurations for the development system.
    current_hyperparameter : tuple
        The current hyperparameters being used in the training process.
    grid_space : Scoreboard
        The scoreboard used to keep track of the classifiers.

    Methods
    -------
    __init__(self, status: DevelopmentSystemStatus, message_bus: MessageBus, configurations: DevelopmentSystemConfigurations)
        Initializes the TrainProcess class with the status, message bus, and configurations.
    set_average_hyperparameters(self)
        Sets the average hyperparameters for the training process.
    receive_learning_set(self)
        Receives the learning set from the message bus.
    get_number_of_iterations(self) -> int
        Gets the number of iterations for the training process.
    remove_precedent_response(self, path: str)
        Removes the previous response from the specified path.
    train(self, current_iteration: int = 0)
        Trains the classifier.
    validate(self)
        Validates the classifier.
    set_next_hyperparamter(self, next_hyperparam: tuple)
        Sets the next hyperparameters for the grid search process.
    set_hyperparams(self)
        Sets the hyperparameters for the training process.
    select_best_classifier(self)
        Selects the best classifier from the grid search.
    perform_grid_search(self)
        Performs a grid search to find the best hyperparameters.
    test_classifier(self)
        Tests the classifier.
    remove_classifiers(self, path: str)
        Removes the classifiers from the specified path.
    """
    # class implementation...class TrainProcess:
    number_of_iterations: int = None
    classifier: Classifier = None
    grid_search: list = None
    hyperparameters: HyperParameterLimit = None
    avg_hyperparameters: dict = None
    status: DevelopmentSystemStatus = None
    learning_set: LearningSet = None
    configurations: DevelopmentSystemConfigurations = None
    current_hyperparameter: tuple = None
    grid_space: Scoreboard = None

    def __init__(
            self,
            status: DevelopmentSystemStatus,
            message_bus: MessageBus,
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

    def set_average_hyperparameters(self):
        print(f'[{self.__class__.__name__}]: setting average hyperparameters')
        self.avg_hyperparameters = {}
        for key in self.configurations.hyperparameters.__dict__:
            self.avg_hyperparameters[key] = (self.configurations.hyperparameters.__dict__[key]['min'] +
                                             self.configurations.hyperparameters.__dict__[key]['max']) // 2
        self.status.average_hyperparameters = self.avg_hyperparameters
        print(
            f'[{self.__class__.__name__}]: average number of neurons: {self.avg_hyperparameters["number_of_neurons"]}')
        print(f'[{self.__class__.__name__}]: average number of layers: {self.avg_hyperparameters["number_of_layers"]}')

    def receive_learning_set(self):
        print(f'[{self.__class__.__name__}]: obtaining learning set from message bus')
        self.learning_set = self.message_bus.popTopic("LearningSet")
        self.status.learning_set = self.learning_set

    def get_number_of_iterations(self) -> int:
        print(f'[{self.__class__.__name__}]: getting number of iterations')
        ret_val = -1
        try:
            with open(f'{os.path.dirname(__file__)}/number_of_iterations.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                JSONValidator(
                    f"{os.path.dirname(__file__)}/../schema/iteration_schema.json").validate_data(data)
                ret_val = data['number_of_iterations']
                self.number_of_iterations = ret_val
                print(
                    f'[{self.__class__.__name__}]: number of iterations read: {ret_val}')
        except FileNotFoundError:  # create file so that AI expert can fill it
            with open(f'{os.path.dirname(__file__)}/number_of_iterations.json', 'w', encoding='utf-8') as json_file:
                json.dump({"number_of_iterations": 0}, json_file)
        finally:
            return ret_val

    def remove_precedent_response(self, path: str):
        ai_expert_response_path = f'{path}.json'
        if os.path.exists(ai_expert_response_path):
            os.remove(ai_expert_response_path)

    def train(self, current_iteration: int = 0):
        print(f'[{self.__class__.__name__}]: starting training classifier')
        if not self.status.should_validate:
            self.classifier = Classifier(
                self.avg_hyperparameters['number_of_neurons'],
                self.avg_hyperparameters['number_of_layers'],
                self.number_of_iterations)
        else:
            self.classifier = Classifier(
                self.current_hyperparameter[0],
                self.current_hyperparameter[1],
                self.status.number_of_iterations,
                f'Classifier {current_iteration}')
        self.classifier.model.fit(
            self.status.learning_set.trainingSet, pd.Series(
                self.status.learning_set.trainingSetLabel))
        if not self.status.should_validate:
            # self.classifier.save_model('classifiers')
            loss_curve = self.classifier.get_loss_curve()
            self.classifier.number_of_iterations = len(loss_curve) + 1
            self.message_bus.pushTopic("learning_plot",
                                       [loss_curve,
                                        self.classifier.number_of_iterations,
                                        self.configurations.loss_threshold])

    def validate(self):
        print(f'[{self.__class__.__name__}]: validating classifier')
        self.classifier.number_of_iterations = len(
            self.classifier.get_loss_curve()) + 1
        y_train_pred = self.classifier.model.predict(
            self.status.learning_set.trainingSet)
        y_val_predicted = self.classifier.model.predict(
            self.status.learning_set.validationSet)
        label_one_hot_encoder = {
            'moderate': [0, 0, 1],
            'normal': [0, 1, 0],
            'high': [1, 0, 0]
        }
        mse = mean_squared_error(
            [label_one_hot_encoder[i] for i in self.status.learning_set.validationSetLabel],
            [label_one_hot_encoder[i] for i in y_val_predicted])

        train_error = 1.0 - \
            accuracy_score(self.status.learning_set.trainingSetLabel, y_train_pred)
        val_error = 1.0 - \
            accuracy_score(self.status.learning_set.validationSetLabel, y_val_predicted)
        self.grid_space.insert_classifier(
            self.classifier, mse, train_error, val_error)

    def set_next_hyperparamter(self, next_hyperparam: tuple):
        self.current_hyperparameter = next_hyperparam

    def set_hyperparams(self):
        print(f'[{self.__class__.__name__}]: creating grid search space')
        layers = []
        for i in range(
                self.configurations.hyperparameters.number_of_layers['min'],
                self.configurations.hyperparameters.number_of_layers['max'] + 1,
                self.configurations.hyperparameters.number_of_layers['step']):
            layers.append(i)
        neurons = []
        for i in range(
                self.configurations.hyperparameters.number_of_neurons['min'],
                self.configurations.hyperparameters.number_of_neurons['max'] + 1,
                self.configurations.hyperparameters.number_of_neurons['step']):
            neurons.append(i)
        self.grid_search = list(itertools.product(layers, neurons))

    def select_best_classifier(self):
        best_models = []
        error_difference = []
        number_of_neurons = []
        number_of_layers = []
        limit = 2
        for i in range(len(self.grid_space.classifiers)):
            current_difference = abs(
                self.grid_space.validation_error[i] -
                self.grid_space.train_error[i])
            if current_difference < self.configurations.overfitting_tolerance:
                best_models.append(self.grid_space.classifiers[i])
                error_difference.append(current_difference)
                number_of_neurons.append(
                    self.grid_space.classifiers[i].number_of_neurons)
                number_of_layers.append(
                    self.grid_space.classifiers[i].number_of_layers)
                if len(best_models) == limit:
                    break

        if len(best_models) == 0:  # none of the classifiers are valid
            self.status.best_classifier_name = "Invalid"
            self.status.best_validation_error = -1.0
            return  # no valid classifier found, skip saving the model
        elif len(best_models) == 1:
            self.classifier = best_models[0]
            self.status.best_validation_error = self.grid_space.validation_error[0]
        elif 0 in error_difference:  # check if one of the error difference is 0 , select that in case
            self.classifier = best_models[error_difference.index(0)]
            self.status.best_validation_error = self.grid_space.validation_error[error_difference.index(
                0)]
        # if there is no significant difference (one order of magnitude)
        # between the two best models
        elif (int(
                math.floor(math.log10
                           (abs(error_difference[0])))) -
              int(math.floor(abs(math.log10(error_difference[1])))) <= 1):
            complexity = []
            for i in range(len(best_models)):
                complexity.append(number_of_layers[i] * number_of_neurons[i])
            self.classifier = best_models[complexity.index(min(complexity))]
            self.status.best_validation_error = self.grid_space.validation_error[complexity.index(
                min(complexity))]
        else:
            self.classifier = best_models[0]
            self.status.best_validation_error = self.grid_space.validation_error[0]
        self.status.best_classifier_name = self.classifier.name
        self.classifier.save_model(
            f'{os.path.dirname(__file__)}/../classifiers')

    def perform_grid_search(self):
        print(f'[{self.__class__.__name__}]: starting grid search')
        iteration = 0  # iteration is used to name the classifiers
        self.grid_space = Scoreboard(self.configurations.classifiers_limit)
        for (number_of_layers, number_of_neurons) in self.grid_search:
            iteration = iteration + 1
            self.set_next_hyperparamter((number_of_layers, number_of_neurons))
            self.train(iteration)
            self.validate()
        self.select_best_classifier()
        # grid search is finished, push the scoreboard in order to obtain
        # validation report
        self.message_bus.pushTopic("Scoreboard", self.grid_space)

    def test_classifier(self):
        print(f'[{self.__class__.__name__}]: testing classifier')
        self.classifier = Classifier()
        self.classifier.load_model(
            f'{os.path.dirname(__file__)}/../classifiers/{self.status.best_classifier_name}')
        y_test_predicted = self.classifier.model.predict(
            self.status.learning_set.testSet)
        test_error = 1.0 - \
            accuracy_score(self.status.learning_set.testSetLabel, y_test_predicted)
        self.message_bus.pushTopic("test_report",
                                   [self.classifier.name,
                                    self.status.best_validation_error,
                                    test_error,
                                    self.configurations.generalization_tolerance])

    def remove_classifiers(self, path: str):
        print(f'[{self.__class__.__name__}]: removing classifiers')
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from src.Development.Classifier import Classifier
from src.Development.Training.HyperParameterLimit import HyperParameterLimit


class TrainProcess:
    number_of_iterations: int = None
    classifier: Classifier = None
    grid_search: GridSearchCV = None
    hyperparameters: HyperParameterLimit = None
    avg_hyperparameters: dict = None

    def set_average_hyperparameters(self):
        avg_hyperparameters = {}
        for key in self.hyperparameters.dict_hyperparameters.keys():
            avg_hyperparameters[key] = (self.hyperparameters.dict_hyperparameters[key][0] +
                                        self.hyperparameters.dict_hyperparameters[key][1]) / 2

    def set_number_of_iterations(self, number_of_iterations: int):
        self.number_of_iterations = number_of_iterations

    def __init__(self, hyperparameters: HyperParameterLimit):
        self.hyperparameters = hyperparameters

    def train(self):
        self.classifier = Classifier(self.avg_hyperparameters['number_of_neurons'],
                                     self.avg_hyperparameters['number_of_layers'])
        self.grid_search = GridSearchCV(self.classifier.model, self.avg_hyperparameters)
        self.grid_search.fit(learning_set, learning_set_labels)
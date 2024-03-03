from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV

from src.Development.Training.HyperParameterLimit import HyperParameterLimit


class TrainProcess:
    number_of_iterations: int = None
    mlp_classifier: MLPClassifier = None
    grid_search: GridSearchCV = None
    hyperparameters: HyperParameterLimit = None
    avg_hyperparameters: dict = None

    def create_hyperparameters_range(self):
        with open('hyperparameters.json', 'r') as file:
            self.hyperparameters = HyperParameterLimit(file.load())

    def set_average_hyperparameters(self) -> dict:
        avg_hyperparameters = {}
        for key in self.hyperparameters.dict_hyperparameters.keys():
            avg_hyperparameters[key] = (self.hyperparameters.dict_hyperparameters[key][0] + self.hyperparameters.dict_hyperparameters[key][1]) / 2
        return avg_hyperparameters
    def set_number_of_iterations(self,number_of_iterations:int):
        self.number_of_iterations=number_of_iterations

    def __init__(self):
        self.mlp_classifier = MLPClassifier()

    def train(self):
        pass

import os

import joblib
from io import BytesIO
from sklearn.neural_network import MLPClassifier


class Classifier:
    name: str = None
    model: MLPClassifier = None
    bytes_container: BytesIO = None
    number_of_neurons: int = None
    number_of_layers: int = None
    number_of_iterations: int = None

    def __init__(self, number_of_neurons: int, number_of_layers: int, number_of_iterations: int,
                 name: str = "AverageClassifier"):
        self.number_of_neurons = number_of_neurons
        self.number_of_layers = number_of_layers
        self.number_of_iterations = number_of_iterations
        self.name = name
        self.model = MLPClassifier(
            hidden_layer_sizes=tuple(self.number_of_neurons for _ in range(self.number_of_layers)),
            max_iter=number_of_iterations)

    def save_model(self, path: str):
        # self.bytes_container = BytesIO()
        # joblib.dump(self.model, self.bytes_container)
        # self.bytes_container.seek(0)
        joblib.dump(self.model, f'{path}/{self.name}.sav')

    def remove_model(self, path: str):
        filename = f'{path}/{self.name}.sav'
        if os.path.exists(filename):
            os.remove(filename)

    def get_loss_curve(self):
        return self.model.loss_curve_

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

    def __init__(self, number_of_neurons: int = 0, number_of_layers: int = 0, number_of_iterations: int = 0,
                 name: str = "AverageClassifier"):
        self.number_of_neurons = number_of_neurons
        self.number_of_layers = number_of_layers
        self.number_of_iterations = number_of_iterations
        self.name = name
        if self.number_of_neurons > 0:
            self.model = MLPClassifier(
                hidden_layer_sizes=tuple(self.number_of_neurons for _ in range(self.number_of_layers)),
                max_iter=number_of_iterations)

    def load_model(self, path: str):
        self.model = joblib.load(f'{path}.sav')
        self.name = path.split('/')[-1]
        self.number_of_iterations = self.model.n_iter_
        self.number_of_layers = self.model.n_layers_
        self.number_of_neurons = len(self.model.coefs_[1]) # trick to get the number of neurons from a model


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

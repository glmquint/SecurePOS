

import joblib
from io import BytesIO
from sklearn.neural_network import MLPClassifier


class Classifier:
    model: MLPClassifier = None
    bytes_container: BytesIO = None
    number_of_neurons: int = None
    number_of_layers: int = None
    number_of_iterations: int = None

    def __init__(self, number_of_neurons: int, number_of_layers: int, number_of_iterations: int):
        self.number_of_neurons = number_of_neurons
        self.number_of_layers = number_of_layers
        self.number_of_iterations = number_of_iterations
        self.model = MLPClassifier(
            hidden_layer_sizes=tuple(self.number_of_neurons for _ in range(self.number_of_layers)),
            max_iter=number_of_iterations)

    def save_model(self, path: str):
        joblib.dump(self.model, path)

    def get_loss_curve(self):
        return self.model.loss_curve_

    def dump_model(self):
        #self.bytes_container = BytesIO()
        #joblib.dump(self.model, self.bytes_container)
        #self.bytes_container.seek(0)
        joblib.dump(self.model, 'Training/classifier.sav')




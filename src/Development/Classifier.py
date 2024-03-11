import joblib
from sklearn.neural_network import MLPClassifier


class Classifier:
    model: MLPClassifier = None
    number_of_neurons: int = None
    number_of_layers: int = None
    number_of_iterations: int = None
    validation_error: float = None

    def __init__(self, number_of_neurons: int, number_of_layers: int, number_of_iterations: int):
        self.number_of_neurons = number_of_neurons
        self.number_of_layers = number_of_layers
        self.number_of_iterations = number_of_iterations
        self.model = MLPClassifier(hidden_layer_sizes=(self.number_of_neurons, self.number_of_layers),
                                   max_iter=number_of_iterations)

    def save_model(self, path: str):
        joblib.dump(self.model, path)

    def get_loss_curve(self):
        return self.model.loss_curve_

from sklearn.neural_network import MLPClassifier


class Classifier:
    model: MLPClassifier = None
    number_of_neurons: int = None
    number_of_layers: int = None

    def __init__(self, number_of_neurons: int, number_of_layers: int):
        self.number_of_neurons = number_of_neurons
        self.number_of_layers = number_of_layers
        self.model = MLPClassifier(hidden_layer_sizes=(self.number_of_neurons, self.number_of_layers))

import joblib
from sklearn.neural_network import MLPClassifier


class Classifier:
    """
    A class used to represent a classifier in the development system.

    Attributes
    ----------
    name : str
        The name of the classifier.
    model : MLPClassifier
        The model of the classifier.
    number_of_neurons : int
        The number of neurons in the classifier.
    number_of_layers : int
        The number of layers in the classifier.
    number_of_iterations : int
        The number of iterations for the classifier.

    Methods
    -------
    __init__(self, number_of_neurons: int = 0, number_of_layers: int = 0, number_of_iterations: int = 0, name: str = "AverageClassifier")
        Initializes the Classifier class with the number of neurons, layers, iterations, and name.
    load_model(self, path: str)
        Loads the model from the specified path.
    save_model(self, path: str)
        Saves the model to the specified path.
    get_loss_curve(self)
        Returns the loss curve of the model.
    """
    # class implementation...class Classifier:
    name: str = None
    model: MLPClassifier = None
    number_of_neurons: int = None
    number_of_layers: int = None
    number_of_iterations: int = None

    def __init__(
            self,
            number_of_neurons: int = 0,
            number_of_layers: int = 0,
            number_of_iterations: int = 0,
            name: str = "AverageClassifier"):
        self.number_of_neurons = number_of_neurons
        self.number_of_layers = number_of_layers
        self.number_of_iterations = number_of_iterations
        self.name = name
        if self.number_of_neurons > 0:
            self.model = MLPClassifier(
                hidden_layer_sizes=tuple(
                    self.number_of_neurons for _ in range(
                        self.number_of_layers)),
                max_iter=number_of_iterations,
                verbose=True)

    def load_model(self, path: str):
        self.model = joblib.load(f'{path}.sav')
        self.name = path.split('/')[-1]
        self.number_of_iterations = self.model.n_iter_
        self.number_of_layers = self.model.n_layers_ - \
            2  # because of input and output layers
        # trick to get the number of neurons from a model
        self.number_of_neurons = len(self.model.coefs_[1])
        print(
            f'[{self.__class__.__name__}]: model loaded successfully from file {path}')

    def save_model(self, path: str):
        joblib.dump(self.model, f'{path}/{self.name}.sav')
        print(
            f'[{self.__class__.__name__}]: model has {self.number_of_layers} layers and {self.number_of_neurons} neurons')
        print(
            f'[{self.__class__.__name__}]: model saved successfully to file {path}/{self.name}.sav')

    def get_loss_curve(self):
        return self.model.loss_curve_

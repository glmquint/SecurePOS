class ValidationRow:
    classifier_name: str = None
    MSE: float = None
    validation_error: float = None
    training_error: float = None
    number_of_layers: int = None
    number_of_neurons: int = None
    error: float = None
    overfitting_tolerance: float = None

    def __init__(self, classifier_name: str, mse: float, validation_error: float, training_error: float,
                 number_of_layers: int,
                 number_of_neurons: int, error: float, overfitting_tolerance: float):
        self.classifier_name = classifier_name
        self.MSE = mse
        self.validation_error = validation_error
        self.training_error = training_error
        self.number_of_layers = number_of_layers
        self.number_of_neurons = number_of_neurons
        self.error = error
        self.overfitting_tolerance = overfitting_tolerance

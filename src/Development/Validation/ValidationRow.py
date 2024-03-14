class ValidationRow:
    classifier_name: str = None
    MSE: float = None
    validation_error: float = None
    training_error: float = None
    number_of_layers: int = None
    number_of_neurons: int = None

    def __init__(self, classifier_name: str, mse: float, validation_error: float, training_error: float,
                 number_of_layers: int,
                 number_of_neurons: int):
        self.classifier_name = classifier_name
        self.MSE = mse
        self.validation_error = validation_error
        self.training_error = training_error
        self.number_of_layers = number_of_layers
        self.number_of_neurons = number_of_neurons

    def to_dict(self):
        return {'classifier_name': self.classifier_name, 'MSE': self.MSE, 'validation_error': self.validation_error,
                'training_error': self.training_error, 'number_of_layers': self.number_of_layers,
                'number_of_neurons': self.number_of_neurons}

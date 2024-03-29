class ValidationRow:
    """
    A class used to model a row in the validation report in the development system.

    Attributes
    ----------
    classifier_name : str
        The name of the classifier.
    MSE : float
        The Mean Squared Error of the classifier.
    validation_error : float
        The validation error of the classifier.
    training_error : float
        The training error of the classifier.
    number_of_layers : int
        The number of layers in the classifier.
    number_of_neurons : int
        The number of neurons in the classifier.

    Methods
    -------
    __init__(self, classifier_name: str, mse: float, validation_error: float, training_error: float, number_of_layers: int, number_of_neurons: int)
        Initializes the ValidationRow class with classifier details.
    to_dict(self)
        Converts the validation row to a dictionary format.
    """
    # class implementation...class ValidationRow:
    classifier_name: str = None
    MSE: float = None
    validation_error: float = None
    training_error: float = None
    number_of_layers: int = None
    number_of_neurons: int = None

    def __init__(
            self,
            classifier_name: str,
            mse: float,
            validation_error: float,
            training_error: float,
            number_of_layers: int,
            number_of_neurons: int):
        self.classifier_name = classifier_name
        self.MSE = mse
        self.validation_error = validation_error
        self.training_error = training_error
        self.number_of_layers = number_of_layers
        self.number_of_neurons = number_of_neurons

    def to_dict(self):
        return {
            'classifier_name': self.classifier_name,
            'MSE': self.MSE,
            'validation_error': self.validation_error,
            'training_error': self.training_error,
            'number_of_layers': self.number_of_layers,
            'number_of_neurons': self.number_of_neurons}

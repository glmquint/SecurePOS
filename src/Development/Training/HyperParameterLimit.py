class HyperParameterLimit:
    """
        A class used to define the limits for the hyperparameters in the development system.

        Attributes
        ----------
        number_of_layers : dict
            The limits for the number of layers in the classifier.
        number_of_neurons : dict
            The limits for the number of neurons in the classifier.

        Methods
        -------
        __init__(self, number_of_layers: dict, number_of_neurons: dict)
            Initializes the HyperParameterLimit class with the limits for the number of layers and neurons.
        """
    # class implementation...class HyperParameterLimit:
    number_of_layers: dict = None
    number_of_neurons: dict = None

    def __init__(self, number_of_layers: dict, number_of_neurons: dict):
        self.number_of_layers = number_of_layers
        self.number_of_neurons = number_of_neurons

class HyperParameterLimit:
    number_of_layers: dict = None
    number_of_neurons: dict = None

    def __init__(self, number_of_layers: dict, number_of_neurons: dict):
        self.number_of_layers = number_of_layers
        self.number_of_neurons = number_of_neurons

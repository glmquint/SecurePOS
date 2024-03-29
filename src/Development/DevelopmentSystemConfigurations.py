import json
from src.Development.Training.HyperParameterLimit import HyperParameterLimit
from src.JsonIO.JsonValidator import JSONValidator


class DevelopmentSystemConfigurations:
    """
    A class used to represent the configurations for the development system.

    Attributes
    ----------
    topics : list
        A list of topics for the development system.
    production_system_receiver : str
        The receiver for the production system.
    messaging_system_receiver : str
        The receiver for the messaging system.
    hyperparameters : HyperParameterLimit
        The hyperparameters for the development system.
    validator : JSONValidator
        The validator for the JSON data.
    loss_threshold : float
        The loss threshold for the development system.
    overfitting_tolerance : float
        The overfitting tolerance for the development system.
    generalization_tolerance : float
        The generalization tolerance for the development system.
    port : int
        The port for the development system.
    endpoint_url : str
        The endpoint URL for the development system.
    classifiers_limit : int
        The limit for the classifiers in the development system.
    stop_and_go : bool
        The stop and go flag for the development system.

    Methods
    -------
    __init__(self, schema_path: str)
        Initializes the DevelopmentSystemConfigurations class.
    update_config(self, data: dict, should_validate: bool = True)
        Updates the configuration with the provided data.
    load_config(self, path: str, should_validate: bool = False)
        Loads the configuration from a JSON file.
    to_dict(self)
        Returns the configuration as a dictionary.
    """
    # class implementation...
    topics: [str] = None
    production_system_receiver: str = None
    messaging_system_receiver: str = None
    hyperparameters: HyperParameterLimit = None
    validator: JSONValidator = None
    loss_threshold: float = None
    overfitting_tolerance: float = None
    generalization_tolerance: float = None
    port: int = None
    endpoint_url: str = None
    classifiers_limit: int = None
    stop_and_go: bool = None

    def __init__(self, schema_path: str):
        self.validator = JSONValidator(schema_path)

    def update_config(self, data: dict, should_validate: bool = True):
        if should_validate:
            self.validator.validate_data(data)
        self.topics = data['topics']
        self.production_system_receiver = data['production_system_receiver']
        self.messaging_system_receiver = data['messaging_system_receiver']
        self.hyperparameters = HyperParameterLimit(
            data['hyperparameters']['number_of_layers'],
            data['hyperparameters']['number_of_neurons'])
        self.loss_threshold = data['loss_threshold']
        self.port = data['port']
        self.endpoint_url = data['endpoint_url']
        self.classifiers_limit = data['classifiers_limit']
        self.overfitting_tolerance = data['overfitting_tolerance']
        self.generalization_tolerance = data['generalization_tolerance']
        self.stop_and_go = data['stop&go']

    def load_config(self, path: str, should_validate: bool = False):
        with open(path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            self.update_config(data, should_validate)
            print(f'[{self.__class__.__name__}]: configurations loaded successfully')

    def to_dict(self):
        return {
            "topics": self.topics,
            "production_system_receiver": self.production_system_receiver,
            "messaging_system_receiver": self.messaging_system_receiver,
            "hyperparameters": self.hyperparameters.__dict__,
            "loss_threshold": self.loss_threshold,
            "overfitting_tolerance": self.overfitting_tolerance,
            "generalization_tolerance": self.generalization_tolerance,
            "port": self.port,
            "endpoint_url": self.endpoint_url,
            "classifiers_limit": self.classifiers_limit,
            "stop&go": self.stop_and_go
        }

import json
from src.Development.Training.HyperParameterLimit import HyperParameterLimit
from src.JsonIO.JsonValidator import JSONValidator


class DevelopmentSystemConfigurations:
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
        self.hyperparameters = HyperParameterLimit(data['hyperparameters']['number_of_layers'],
                                                   data['hyperparameters']['number_of_neurons'])
        self.loss_threshold = data['loss_threshold']
        self.port = data['port']
        self.endpoint_url = data['endpoint_url']
        self.classifiers_limit = data['classifiers_limit']
        self.overfitting_tolerance = data['overfitting_tolerance']
        self.generalization_tolerance = data['generalization_tolerance']
        self.stop_and_go = data['stop&go']

    def load_config(self, path: str, should_validate: bool = False):
        with open(path, 'r') as json_file:
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
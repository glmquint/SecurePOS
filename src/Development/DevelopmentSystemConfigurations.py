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

    def load_config(self, path: str, should_validate: bool = False):
        with open(path, 'r') as json_file:
            data = json.load(json_file)
            self.update_config(data, should_validate)

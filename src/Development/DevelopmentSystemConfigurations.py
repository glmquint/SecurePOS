import json

from src.Development.Training.HyperParameterLimit import HyperParameterLimit


class DevelopmentSystemConfigurations:
    ip: str
    port: int
    hyperparameters: HyperParameterLimit

    def __init__(self):
        with open('config.json') as json_file:  # validate config.json
            data = json.load(json_file)
            self.ip = data['ip']
            self.port = data['port']
            self.hyperparameters = data['hyperparameters']

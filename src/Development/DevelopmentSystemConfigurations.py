import json


class DevelopmentSystemConfigurations:
    ip: str
    port: int
    hyperparameters: dict

    def __init__(self):
        # read from json file
        with open('config.json') as json_file:
            data = json.load(json_file)
            self.ip = data['ip']
            self.port = data['port']
            self.hyperparameters = data['hyperparameters']

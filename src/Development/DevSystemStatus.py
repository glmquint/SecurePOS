import json


class DevSystemStatus:
    status: str
    should_validate: bool

    def __init__(self, status: str = "OK", should_validate: bool = False):
        self.status = status
        self.should_validate = should_validate

    def load_status(self, path: str):
        with open(path, 'r') as json_file:
            data = json.load(json_file)
            self.status = data['status']
            self.should_validate = data['should_validate']

    def save_status(self, status: str, should_validate: bool, path: str):
        self.status = status
        self.should_validate = should_validate
        with open(path, 'w') as json_file:
            json.dump(self.__dict__, json_file)

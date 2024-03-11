import json

from src.Development.LearningSet import LearningSet
from src.JsonIO.JsonValidator import JSONValidator


class DevelopmentSystemStatus:
    status: str
    should_validate: bool
    average_hyperparameters: dict
    learning_set: LearningSet
    schema_path: str
    status_path: str
    validator: JSONValidator

    def __init__(self, status_file_path: str, validation_schema_path: str):
        self.status_path = status_file_path
        self.schema_path = validation_schema_path
        self.validator = JSONValidator(self.schema_path)

    def load_status(self):
        try:
            with open(self.status_path, 'r') as json_file:
                data = json.load(json_file)
                self.validator.validate_data(data)
                self.status = data['status']
                self.should_validate = data['should_validate']
                self.learning_set = LearningSet(json.loads(data['learning_set']))
                self.average_hyperparameters = data['average_hyperparameters']
        except FileNotFoundError as e:
            self.status = "receive_learning_set"
            self.should_validate = False

    def to_dict(self):
        return dict(status=self.status, should_validate=self.should_validate,
                    average_hyperparameters=self.average_hyperparameters, learning_set=self.learning_set.json())

    def save_status(self):
        with open(self.status_path, 'w') as json_file:
            json.dump(self.to_dict(), json_file)
            exit(0)

# dev_status = DevSystemStatus()
# print(dev_status.__dict__)
# dev_status.save_status("2", True)
# dev_status2 = DevSystemStatus()
# dev_status2.load_status()
# print(dev_status2.__dict__)

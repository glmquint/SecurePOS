import json

from src.DataObjects.LearningSet import LearningSet
from src.JsonIO.JsonValidator import JSONValidator


class DevelopmentSystemStatus:
    status: str
    should_validate: bool
    average_hyperparameters: dict = None
    learning_set: LearningSet = None
    number_of_iterations: int = -1
    best_classifier_name: str = ""
    best_validation_error: float = 0.0
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
                if 'learning_set' in data.keys():
                    self.learning_set = LearningSet(data['learning_set'], True)
                if 'average_hyperparameters' in data.keys():
                    self.average_hyperparameters = data['average_hyperparameters']
                if 'number_of_iterations' in data.keys():
                    self.number_of_iterations = data['number_of_iterations']
                if 'best_classifier_name' in data.keys():
                    self.best_classifier_name = data['best_classifier_name']
                if 'best_validation_error' in data.keys():
                    self.best_validation_error = data['best_validation_error']
        except FileNotFoundError as e:
            self.status = "receive_learning_set"
            self.should_validate = False

    def to_dict(self):
        return dict(status=self.status, should_validate=self.should_validate,
                    average_hyperparameters=self.average_hyperparameters,
                    number_of_iterations=self.number_of_iterations, learning_set=self.learning_set.to_json(),
                    best_classifier_name=self.best_classifier_name, best_validation_error=self.best_validation_error)

    def save_status(self):
        with open(self.status_path, 'w') as json_file:
            json.dump(self.to_dict(), json_file, indent=4)
            exit(0)

import json
import os

from src.JsonIO.JsonValidator import JSONValidator


class EvaluationSystemConfig:
    """
        This class is responsible for managing the configuration of the evaluation system. It loads the configuration from a
        JSON file, validates the data, and provides access to the configuration values.

        Attributes:
            sufficient_label_number: The sufficient number of labels for the evaluation.
            simulate_human_task: A boolean value that indicates whether to simulate a human task.
            state: The current state of the system.
            path_config_validator: The path to the JSON validator.
            path_config: The path to the configuration file.
            tollerated_error: The tolerated error in the evaluation.
            tollerated_consecutive_error: The tolerated consecutive error in the evaluation.
            port: The port number.
            messaging_ip: The IP address for messaging.
            messaging_port: The port number for messaging.

        Methods:
            write_state: Writes the state to the JSON file.
            load: Loads the configuration from the JSON file and validates the data.
    """
    def __init__(
            self,
            path_config: str = f"{os.path.dirname(__file__)}/config/config.json"):
        self.sufficient_label_number = 0
        self.simulate_human_task = False
        self.state = 0
        self.path_config_validator = f"{os.path.dirname(__file__)}/config/validator.json"
        self.path_config = path_config
        self.tollerated_error = 0
        self.tollerated_consecutive_error = 0
        self.port = 0
        self.messaging_ip = ""
        self.messaging_port = 0
        self.load()

    def write_state(self, state=0):
        """this function write on json file"""
        with open(self.path_config, "r") as json_file:
            data = json.load(json_file)

        data["state"] = state

        with open(self.path_config, "w") as json_file:
            json.dump(data, json_file, indent=4)

        self.state = state

    def load(self):
        """load from a json file the configuration"""
        validator = JSONValidator(self.path_config_validator)
        file = open(self.path_config)
        data = json.load(file)
        file.close()
        validator.validate_data(data)

        self.sufficient_label_number = data["sufficient_label_number"]
        self.state = data["state"]
        self.tollerated_error = data["tollerated_error"]
        self.tollerated_consecutive_error = data["tollerated_consecutive_error"]
        self.port = data["port"]
        self.messaging_ip = data["messaging_ip"]
        self.messaging_port = data["messaging_port"]
        if data["simulate_human_task"] == "True":
            self.simulate_human_task = True
        else:
            self.simulate_human_task = False
        file.close()

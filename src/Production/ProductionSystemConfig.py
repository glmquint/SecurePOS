import json
import os

from src.JsonIO.JsonValidator import JSONValidator


class ProductionSystemConfig:
    """
       This class is responsible for storing and managing the configuration of the production system.
       It reads the configuration from a JSON file and validates it against a schema.

       Attributes:
           config: A dictionary that stores the configuration values.
           server_port: The port on which the server is running.
           monitoring_window: The time window for monitoring phase.
           evaluation_window: The time window for evaluating phase.
           client_url: The URL of the client.
           evaluation_url: The URL for evaluation.
           message_url: The URL for sending messages.
           phase: The current phase of the system.
       """
    def __init__(
            self,
            path_to_config,
            path_to_schema: str = f'{os.path.dirname(__file__)}/config/configSchema.json'):
        # Open the configuration file and read the values
        try:
            with open(path_to_config, 'r') as file:
                self.config = json.load(file)
                json_validator = JSONValidator(path_to_schema)
                json_validator.validate_data(self.config)
                self.server_port = self.config['server_port']
                self.monitoring_window = self.config['monitoring_window']
                self.evaluation_window = self.config['evaluation_window']
                self.client_url = self.config['client_url']
                self.evaluation_url = self.config['evaluation_url']
                self.message_url = self.config['message_url']
                self.phase = self.config['phase']
        except Exception as e:
            print("An error occurred:", e)

    # A print function for the configuration
    def __str__(self):
        return f"Monitoring Window: {self.monitoring_window},\nEvaluation Window: {self.evaluation_window},\n" \
               f"Client URL: {self.client_url},\nEvaluation URL: {self.evaluation_url}"

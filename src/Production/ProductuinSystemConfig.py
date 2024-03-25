# A class for storing the configuration of the production system
import json

from src.JsonIO.JsonValidator import JSONValidator


class ProductionSystemConfig:
    def __init__(self, path_to_config, path_to_schema):
        # Open the configuration file and read the values
        try:
            with open(path_to_config, 'r') as file:
                self.config = json.load(file)
                jsonValidator = JSONValidator(path_to_schema)
                jsonValidator.validate_data(self.config)
                self.server_port = self.config['server_port']
                self.monitoring_window = self.config['monitoring_window']
                self.evaluation_window = self.config['evaluation_window']
                self.client_url = self.config['client_url']
                self.evaluation_url = self.config['evaluation_url']
                self.message_url = self.config['message_url']
        except Exception as e:
            print("An error occurred:", e)

    # A print function for the configuration
    def __str__(self):
        return f"Monitoring Window: {self.monitoring_window},\nEvaluation Window: {self.evaluation_window},\n" \
               f"Client URL: {self.client_url},\nEvaluation URL: {self.evaluation_url}"


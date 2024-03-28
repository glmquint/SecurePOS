import json
import os

from src.JsonIO.JsonValidator import JSONValidator


class SegregationSystemConfig:
    def __init__(self, config_path: str = f'{os.path.dirname(__file__)}/Configurations/segregationConfiguration.json',
                 validate_path: str = f"{os.path.dirname(__file__)}/../DataObjects/Schema"
                                      f"/SegregationSystemConfigSchema.json"
                 ):
        json_parameter = None
        with open(config_path, 'r') as file:
            json_parameter = json.load(file)

        validator = JSONValidator(validate_path)
        validator.validate_data(json_parameter)

        self.__sufficient_session_number = json_parameter.get("sufficientSessionNumber")
        self.__segregation_system_port = json_parameter.get("segregationSystemPort")
        self.__segregation_system_endpoint = json_parameter.get("segregationSystemEndpoint")
        self.__development_system_ip = json_parameter.get("developmentSystemIp")
        self.__development_system_port = json_parameter.get("developmentSystemPort")
        self.__development_system_endpoint = json_parameter.get("developmentSystemEndpoint")
        self.__tolerance_data_balancing = json_parameter.get("toleranceDataBalancing")
        self.__service_flag = json_parameter.get("serviceFlag")
        self.__percentage_training_split = json_parameter.get("percentageTrainingSplit")
        self.__percentage_test_split = json_parameter.get("percentageTestSplit")
        self.__percentage_validation_split = json_parameter.get("percentageValidationSplit")

        self.__messaging_system_ip = json_parameter.get("messagingSystemIp")
        self.__messaging__system_port = json_parameter.get("messagingSystemPort")
        self.__messaging__system_endpoint = json_parameter.get("messagingSystemEndpoint")

    def get_sufficient_session_number(self):
        return self.__sufficient_session_number

    def get_segregation_system_port(self):
        return self.__segregation_system_port

    def get_development_system_ip(self):
        return self.__development_system_ip

    def get_development_system_port(self):
        return self.__development_system_port

    def get_tolerance_data_balancing(self):
        return self.__tolerance_data_balancing

    def get_service_flag(self):
        return self.__service_flag

    def get_percentage_training_split(self):
        return self.__percentage_training_split

    def get_percentage_test_split(self):
        return self.__percentage_test_split

    def get_percentage_validation_split(self):
        return self.__percentage_validation_split

    def get_development_system_endpoint(self):
        return self.__development_system_endpoint

    def get_segregation_system_endpoint(self):
        return self.__segregation_system_endpoint

    def get_messaging_system_ip(self):
        return self.__messaging_system_ip

    def get_messaging_system_port(self):
        return self.__messaging__system_port

    def get_messaging_system_endpoint(self):
        return self.__messaging__system_endpoint

    def to_json(self):
        return self.__dict__

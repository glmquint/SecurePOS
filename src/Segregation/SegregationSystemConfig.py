import json
import os


class SegregationSystemConfig:
    def __init__(self, config_path: str = f'{os.path.dirname(__file__)}/Configurations/segregationConfiguration.json'):

        with open(config_path, 'r') as file:
            jsonParameter = json.load(file)

        self.__sufficient_session_number = jsonParameter.get("sufficientSessionNumber")
        self.__segregation_system_port = jsonParameter.get("segregationSystemPort")
        self.__segregation_system_endpoint = jsonParameter.get("segregationSystemEndpoint")
        self.__developmentSystemIp = jsonParameter.get("developmentSystemIp")
        self.__development_system_port = jsonParameter.get("developmentSystemPort")
        self.__development_system_endpoint = jsonParameter.get("developmentSystemEndpoint")
        self.__tolerance_data_balancing = jsonParameter.get("toleranceDataBalancing")
        self.__service_flag = jsonParameter.get("serviceFlag")
        self.__percentage_training_split = jsonParameter.get("percentageTrainingSplit")
        self.__percentage_test_split = jsonParameter.get("percentageTestSplit")
        self.__percentage_validation_split = jsonParameter.get("percentageValidationSplit")

        self.__messaging_SystemIp = jsonParameter.get("messagingSystemIp")
        self.__messaging__system_port = jsonParameter.get("messagingSystemPort")
        self.__messaging__system_endpoint = jsonParameter.get("messagingSystemEndpoint")

    def get_sufficient_session_number(self):
        return self.__sufficient_session_number

    def get_segregation_system_port(self):
        return self.__segregation_system_port

    def get_development_system_ip(self):
        return self.__developmentSystemIp

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
        return self.__messaging_SystemIp

    def get_messaging_system_port(self):
        return self.__messaging__system_port

    def get_messaging_system_endpoint(self):
        return self.__messaging__system_endpoint

    def to_json(self):
        return self.__dict__
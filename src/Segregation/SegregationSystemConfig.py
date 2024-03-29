import json
import os
from src.JsonIO.JsonValidator import JSONValidator

class SegregationSystemConfig:
    """
    Class responsible for handling the configuration settings of the segregation system.

    Attributes:
    __sufficient_session_number (int): The number of sessions considered sufficient.
    __segregation_system_port (int): The port number of the segregation system.
    __segregation_system_endpoint (str): The endpoint of the segregation system.
    __development_system_ip (str): The IP address of the development system.
    __development_system_port (int): The port number of the development system.
    __development_system_endpoint (str): The endpoint of the development system.
    __tolerance_data_balancing (float): The tolerance parameter for data balancing.
    __service_flag (bool): Flag to indicate whether the service is active or not.
    __percentage_training_split (float): Percentage of data to be used for training.
    __percentage_test_split (float): Percentage of data to be used for testing.
    __percentage_validation_split (float): Percentage of data to be used for validation.
    __messaging_system_ip (str): The IP address of the messaging system.
    __messaging_system_port (int): The port number of the messaging system.
    __messaging_system_endpoint (str): The endpoint of the messaging system.

    Methods:
    get_sufficient_session_number(): Returns the sufficient session number.
    get_segregation_system_port(): Returns the segregation system port.
    get_development_system_ip(): Returns the development system IP.
    get_development_system_port(): Returns the development system port.
    get_tolerance_data_balancing(): Returns the data balancing tolerance.
    get_service_flag(): Returns the service flag.
    get_percentage_training_split(): Returns the training split percentage.
    get_percentage_test_split(): Returns the test split percentage.
    get_percentage_validation_split(): Returns the validation split percentage.
    get_development_system_endpoint(): Returns the development system endpoint.
    get_segregation_system_endpoint(): Returns the segregation system endpoint.
    get_messaging_system_ip(): Returns the messaging system IP.
    get_messaging_system_port(): Returns the messaging system port.
    get_messaging_system_endpoint(): Returns the messaging system endpoint.
    to_json(): Converts the configuration object to a JSON format.
    """

    def __init__(
            self,
            config_path: str = f'{os.path.dirname(__file__)}/Configurations/segregationConfiguration.json',
            validate_path: str = f"{os.path.dirname(__file__)}/../DataObjects/Schema/SegregationSystemConfigSchema.json"):
        """
        Initializes the SegregationSystemConfig with the provided configuration and validation paths.

        Parameters:
        config_path (str): The path to the segregation system configuration file.
        validate_path (str): The path to the schema for validation.
        """
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
        self.__messaging_system_port = json_parameter.get("messagingSystemPort")
        self.__messaging_system_endpoint = json_parameter.get("messagingSystemEndpoint")

    # Getter methods for all attributes
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
        return self.__messaging_system_port

    def get_messaging_system_endpoint(self):
        return self.__messaging_system_endpoint

    def to_json(self) -> str:
        """
        Converts the configuration object to a JSON format.

        Returns:
        str: JSON representation of the configuration object.
        """
        config_dict = {
            "sufficientSessionNumber": self.__sufficient_session_number,
            "segregationSystemPort": self.__segregation_system_port,
            "segregationSystemEndpoint": self.__segregation_system_endpoint,
            "developmentSystemIp": self.__development_system_ip,
            "developmentSystemPort": self.__development_system_port,
            "developmentSystemEndpoint": self.__development_system_endpoint,
            "toleranceDataBalancing": self.__tolerance_data_balancing,
            "serviceFlag": self.__service_flag,
            "percentageTrainingSplit": self.__percentage_training_split,
            "percentageTestSplit": self.__percentage_test_split,
            "percentageValidationSplit": self.__percentage_validation_split,
            "messagingSystemIp": self.__messaging_system_ip,
            "messagingSystemPort": self.__messaging_system_port,
            "messagingSystemEndpoint": self.__messaging_system_endpoint
        }
        return config_dict

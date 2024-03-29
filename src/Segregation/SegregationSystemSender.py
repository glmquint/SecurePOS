import json
import os

from src.JsonIO.JSONSender import JSONSender
from src.Segregation.SegregationSystemConfig import SegregationSystemConfig
from src.util import monitorPerformance, Message


class SegregationSystemSender:
    """
    Class responsible for sending data to the development and messaging systems.

    Attributes:
    __development_sender (JSONSender): An instance of JSONSender for sending
                                        data to the development system.
    __messaging_sender (JSONSender): An instance of JSONSender for sending
                                            data to the messaging system.
    __config_parameter (SegregationSystemConfig): An instance of SegregationSystemConfig
                                                containing configuration parameters.
    __learning_set_generator: An instance of learningSetGenerator to generate learning sets.
    """

    def __init__(self, config: SegregationSystemConfig, learning_set_generator):
        """
        Initializes the SegregationSystemSender with the given parameters.

        Parameters:
        config (SegregationSystemConfig): An instance of SegregationSystemConfig
        containing configuration parameters.
        learningSetGenerator: An instance to generate learning sets.
        """
        self.__config_parameter = config

        development_system_ip = self.__config_parameter.get_development_system_ip()
        development_system_port = self.__config_parameter.get_development_system_port()
        development_system_endpoint = self.__config_parameter.get_development_system_endpoint()
        self.__development_sender = JSONSender(
            f"{os.path.dirname(__file__)}/../DataObjects/Schema/learning_set_schema.json",
            f"http://{development_system_ip}:{development_system_port}/{development_system_endpoint}")

        messaging_system_ip = self.__config_parameter.get_messaging_system_ip()
        messaging_system_port = self.__config_parameter.get_messaging_system_port()
        messaging_system_endpoint = self.__config_parameter.get_messaging_system_endpoint()
        self.__messaging_sender = JSONSender(
            f"{os.path.dirname(__file__)}/../DataObjects/Schema/MessageSchema.json",
            f"http://{messaging_system_ip}:{messaging_system_port}/{messaging_system_endpoint}")

        self.__learning_set_generator = learning_set_generator

    @monitorPerformance(should_sample_after=True)
    def send_to_development(self):
        """
        Sends the learning set to the development system.
        """
        learning_set = self.__learning_set_generator.leaning_set
        print(learning_set.to_json())
        self.__development_sender.send(learning_set)

    @monitorPerformance(should_sample_after=True)
    def send_to_messaging(self):
        """
        Sends the configuration parameters to the messaging system.
        """
        self.__messaging_sender.send(
            Message(
                msg=json.dumps(
                    self.__config_parameter.to_json())))

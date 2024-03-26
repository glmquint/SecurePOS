import os

from src.JsonIO.JSONSender import JSONSender
from src.Segregation.SegregationSystemConfig import SegregationSystemConfig
from src.util import monitorPerformance


class SegregationSystemSender:
    __development_sender = None
    __messaging_sender = None
    __messageBus = None
    __config_parameter = None

    def __init__(self, config : SegregationSystemConfig, learningSetGenerator):
        self.__config_parameter = config

        development_system_ip = self.__config_parameter.get_development_system_ip()
        development_system_port = self.__config_parameter.get_development_system_port()
        development_system_endpoint = self.__config_parameter.get_development_system_endpoint()
        self.__development_sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/learning_set_schema.json",
                                               "http://" + str(development_system_ip) + ":" + str(
                                                   development_system_port) + "/" + str(
                                                   development_system_endpoint))

        messaging_system_ip = self.__config_parameter.get_messaging_system_ip()
        messaging_system_port = self.__config_parameter.get_messaging_system_port()
        messaging_system_endpoint = self.__config_parameter.get_messaging_system_endpoint()
        self.__messaging_system = JSONSender(
            f"{os.path.dirname(__file__)}/../DataObjects/Schema/learning_set_schema.json",
            "http://" + str(messaging_system_ip) + ":" + str(
                messaging_system_port) + "/" + str(
                messaging_system_endpoint))
        self.__learning_set_generator = learningSetGenerator

    @monitorPerformance(should_sample_after=True)
    def send_to_development(self):
        learning_set = self.__learning_set_generator.leaning_set
        print(learning_set.to_json())
        self.__development_sender.send(learning_set)

    @monitorPerformance(should_sample_after=True)
    def send_to_messaging(self):
        self.__messaging_system.send(self.__config_parameter)

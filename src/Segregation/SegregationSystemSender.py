import os

from src.JsonIO.JSONSender import JSONSender
from src.Segregation.SegregationSystemConfig import SegregationSystemConfig
from src.util import monitorPerformance


class SegregationSystemSender:
    __development_sender = None
    __messageBus = None

    def __init__(self, learningSetGenerator):
        config_parameter = SegregationSystemConfig()

        self.__development_system_ip = config_parameter.get_development_system_ip()
        self.__development_system_port = config_parameter.get_development_system_port()
        self.__development_system_endpoint = config_parameter.get_development_system_endpoint()
        self.__development_sender = JSONSender(f"{os.path.dirname(__file__)}/../DataObjects/Schema/learning_set_schema.json",
                                               "http://" + self.__development_system_ip + ":" + str(
                                                   self.__development_system_port) + "/" + str(
                                                   self.__development_system_endpoint))

        self.__learning_set_generator = learningSetGenerator

    @monitorPerformance(should_sample_after=True)
    def send_to_development(self):
        learning_set = self.__learning_set_generator.leaning_set
        print(learning_set.to_json())
        self.__development_sender.send(learning_set)

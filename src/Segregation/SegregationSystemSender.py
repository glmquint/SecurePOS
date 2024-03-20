from src.JsonIO.JSONSender import JSONSender
from src.Segregation.SegregationSystemConfig import SegregationSystemConfig


class SegregationSystemSender:
    __DevelopmentSender = None
    __messageBus = None

    def __init__(self, learningSetGenerator):
        configParameter = SegregationSystemConfig()

        developmentSystemIp = configParameter.getDevelopmentSystemIp()
        developmentSystemPort = configParameter.getDevelopmentSystemPort()
        developmentSystemEndpoint = configParameter.getDevelopmentSystemEndpoint()
        self.__DevelopmentSender = JSONSender("../DataObjects/Schema/learning_set_schema.json",
                                              "http://" + developmentSystemIp + ":" + str(
                                                  developmentSystemPort) + "/" + str(developmentSystemEndpoint))

        self.__learningSetGenerator = learningSetGenerator

    def send_to_development(self):
        learning_set = self.__learningSetGenerator.leaning_set
        print(learning_set.to_json())
        self.__DevelopmentSender.send(learning_set)

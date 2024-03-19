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
        self.__DevelopmentSender = JSONSender("../DataObjects/Schema/LearningSetSchema.json",
                                              "http://" + developmentSystemIp + ":" + str(
                                                  developmentSystemPort) + "/" + str(developmentSystemEndpoint))

        self.__learningSetGenerator = learningSetGenerator

    def sendToDevelopment(self):
        learning_set = self.__learningSetGenerator.leaning_set
        self.__DevelopmentSender.send(learning_set.toJson())

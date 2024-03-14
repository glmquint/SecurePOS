from src.JsonIO.JSONSender import JSONSender
from src.Segregation.SegregationSystemConfig import SegregationSystemConfig


class SegregationSystemSender:
    __DevelopmentSender = None
    __messageBus = None

    def __init__(self, messageBus):
        configParameter = SegregationSystemConfig()

        developmentSystemIp = configParameter.getDevelopmentSystemIp()
        developmentSystemPort = configParameter.getDevelopmentSystemPort()
        developmentSystemEndpoint = configParameter.getDevelopmentSystemEndpoint()
        self.__DevelopmentSender = JSONSender("../DataObjects/Schema/LearningSetSchema.json",
                                              "http://" + developmentSystemIp + ":" + str(
                                                  developmentSystemPort) + "/" + str(developmentSystemEndpoint))

        self.__messageBus = messageBus

    def sendToDevelopment(self):
        learningSet = self.__messageBus.popTopic("leaningSet")
        self.__DevelopmentSender.send(learningSet.toJson())

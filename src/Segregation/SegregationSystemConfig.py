import json


class SegregationSystemConfig:
    def __init__(self):
        with open('Configurations/segregationConfiguration.json', 'r') as file:
            jsonParameter = json.load(file)
        self.__sufficientSessionNumber = jsonParameter.get("sufficientSessionNumber")
        self.__segregationSystemPort = jsonParameter.get("segregationSystemPort")
        self.__developmentSystemIp = jsonParameter.get("developmentSystemIp")
        self.__developmentSystemPort = jsonParameter.get("developmentSystemPort")
        self.__developmentSystemEndpoint = jsonParameter.get("developmentSystemEndpoint")
        self.__toleranceDataBalancing = jsonParameter.get("toleranceDataBalancing")
        self.__serviceFlag = jsonParameter.get("serviceFlag")
        self.__percentageTrainingSplit = jsonParameter.get("percentageTrainingSplit")
        self.__percentageTestSplit = jsonParameter.get("percentageTestSplit")
        self.__percentageValidationSplit = jsonParameter.get("percentageValidationSplit")

    def getSufficientSessionNumber(self):
        return self.__sufficientSessionNumber

    def getSegregationSystemPort(self):
        return self.__segregationSystemPort

    def getDevelopmentSystemIp(self):
        return self.__developmentSystemIp

    def getDevelopmentSystemPort(self):
        return self.__developmentSystemPort

    def getToleranceDataBalancing(self):
        return self.__toleranceDataBalancing

    def getServiceFlag(self):
        return self.__serviceFlag

    def getPercentageTrainingSplit(self):
        return self.__percentageTrainingSplit

    def getPercentageTestSplit(self):
        return self.__percentageTestSplit

    def getPercentageValidationSplit(self):
        return self.__percentageValidationSplit

    def getDevelopmentSystemEndpoint(self):
        return self.__developmentSystemEndpoint


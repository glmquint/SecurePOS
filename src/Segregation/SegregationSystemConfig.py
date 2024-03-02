import json


class SegregationSystemConfig:
    def __init__(self):
        with open('Configurations/segregationConfiguration.json', 'r') as file:
            jsonParameter = json.load(file)
        self.__sufficientSessionNumber = jsonParameter.get("sufficientSessionNumber")
        self.__segregationSystemIp = jsonParameter.get("segregationSystemIp")
        self.__segregationSystemPort = jsonParameter.get("segregationSystemPort")
        self.__developmentSystemIp = jsonParameter.get("developmentSystemIp")
        self.__developmentSystemPort = jsonParameter.get("developmentSystemPort")
        self.__toleraceDataBalancing = jsonParameter.get("toleraceDataBalancing")
        self.__serviceFlag = jsonParameter.get("serviceFlag")
        self.__percentageTrainingSplit = jsonParameter.get("percentageTrainingSplit")
        self.__percentageTestSplit = jsonParameter.get("percentageTestSplit")
        self.__percentageValidationSplit = jsonParameter.get("percentageValidationSplit")

    def getSufficientSessionNumber(self):
        return self.__sufficientSessionNumber

    def getSegregationSystemIp(self):
        return self.__segregationSystemIp

    def geSegregationSystemPort(self):
        return self.__segregationSystemPort

    def getDevelopmentSystemIp(self):
        return self.__developmentSystemIp

    def getDevelopmentSystemPort(self):
        return self.__developmentSystemPort

    def getToleranceDataBalancing(self):
        return self.__toleraceDataBalancing

    def getServiceFlag(self):
        return self.__serviceFlag

    def getPercentageTrainingSplit(self):
        return self.__percentageTrainingSplit

    def getPercentageTestSplit(self):
        return self.__percentageTestSplit

    def getPercentageValidationSplit(self):
        return self.__percentageValidationSplit

class PreparedSession:

    def __init__(self, params):
        if type(params) is not dict:  # this if i create a preparedSession from a list
            self.__UUID = params[0]
            self.__MeanAbsoluteDifferencingTransactionTimestamps = params[1]
            self.__MeanAbsoluteDifferencingTransactionAmount = params[2]
            self.__MedianLongitude = params[3]
            self.__MedianLatitude = params[4]
            self.__MedianTargetIP = params[5]
            self.__MedianDestIP = params[6]
            self.__Label = params[7]
        else:
            self.__dict__ = params

    def returnArray(self):
        return [self.__UUID, self.__MeanAbsoluteDifferencingTransactionTimestamps,
                self.__MeanAbsoluteDifferencingTransactionAmount,
                self.__MedianLongitude, self.__MedianLatitude, self.__MedianTargetIP, self.__MedianDestIP, self.__Label]

    def getUUID(self):
        return self.__UUID

    def getMeanAbsoluteDifferencingTransactionTimestamps(self):
        return self.__MeanAbsoluteDifferencingTransactionTimestamps

    def getMeanAbsoluteDifferencingTransactionAmount(self):
        return self.__MeanAbsoluteDifferencingTransactionAmount

    def getMedianLongitude(self):
        return self.__MedianLongitude

    def getMedianLatitude(self):
        return self.__MedianLatitude

    def getMedianTargetIP(self):
        return self.__MedianTargetIP

    def getMedianDestIP(self):
        return self.__MedianDestIP

    def getLabel(self):
        return self.__Label

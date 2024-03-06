class PreparedSession:

    def __init__(self, params):
        if type(params) != dict:  # this if a create a preparedSession from a list
            self.MeanAbsoluteDifferencingTransactionTimestamps = params[0]
            self.MeanAbsoluteDifferencingTransactionAmount = params[1]
            self.MedianLongitude = params[2]
            self.MedianLatitude = params[3]
            self.MedianTargetIP = params[4]
            self.MedianDestIP = params[5]
            self.label = params[6]
        else:
            self.__dict__ = params

    def returnArray(self):
        return [self.MeanAbsoluteDifferencingTransactionTimestamps, self.MeanAbsoluteDifferencingTransactionAmount,
                self.MedianLongitude, self.MedianLatitude, self.MedianTargetIP, self.MedianDestIP, self.label]

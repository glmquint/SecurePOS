class PreparedSession:


    def ok(self, params):
        self.MeanAbsoluteDifferencingTransactionTimestamps = params[0]
        self.MeanAbsoluteDifferencingTransactionAmount = params[1]
        self.MedianLongitude = params[2]
        self.MedianLatitude = params[3]
        self.MedianTargetIP = params[4]
        self.MedianDestIP = params[5]
        self.label = params[6]

    def __init__(self, d):
        self.__dict__ = d

    def returnArray(self):
        return [self.MeanAbsoluteDifferencingTransactionTimestamps,self.MeanAbsoluteDifferencingTransactionAmount,self.MedianLongitude,self.MedianLatitude,self.MedianTargetIP,self.MedianDestIP,self.label]


class PreparedSession:
    MeanAbsoluteDifferencingTransactionTimestamps = 0
    MeanAbsoluteDifferencingTransactionAmount = 0
    MedianLongitude = 0
    MedianLatitude = 0
    MedianTargetIP = 0
    MedianDestIP = 0
    label = ""
    def __init__(self,selfMeanAbsoluteDifferencingTransactionTimestamps,MeanAbsoluteDifferencingTransactionAmount,MedianLongitude,MedianLatitude,MedianTargetIP,MedianDestIP,label):
        self.MeanAbsoluteDifferencingTransactionTimestamps = selfMeanAbsoluteDifferencingTransactionTimestamps
        self.MeanAbsoluteDifferencingTransactionAmount = MeanAbsoluteDifferencingTransactionAmount
        self.MedianLongitude = MedianLongitude
        self.MedianLatitude = MedianLatitude
        self.MedianTargetIP = MedianTargetIP
        self.MedianDestIP =  MedianDestIP
        self.label = label

    def ko(self, params):
        self.MeanAbsoluteDifferencingTransactionTimestamps = params[0]
        self.MeanAbsoluteDifferencingTransactionAmount = params[1]
        self.MedianLongitude = params[2]
        self.MedianLatitude = params[3]
        self.MedianTargetIP = params[4]
        self.MedianDestIP = params[5]
        self.label = params[6]

    def returnArray(self):
        return [self.MeanAbsoluteDifferencingTransactionTimestamps,self.MeanAbsoluteDifferencingTransactionAmount,self.MedianLongitude,self.MedianLatitude,self.MedianTargetIP,self.MedianDestIP,self.label]
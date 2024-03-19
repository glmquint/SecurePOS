class PreparedSession:
    label = None
    median_dest_ip = None
    median_target_ip = None
    median_latitude = None
    median_longitude = None
    mean_absolute_differencing_transaction_amount = None
    mean_absolute_differencing_transaction_timestamps = None

    def __init__(self, params):
        if type(params) is not dict:  # this if i create a preparedSession from a list
            self.mean_absolute_differencing_transaction_timestamps = params[0]
            self.mean_absolute_differencing_transaction_amount = params[1]
            self.median_longitude = params[2]
            self.median_latitude = params[3]
            self.median_target_ip = params[4]
            self.median_dest_ip = params[5]
            self.label = params[6]
        else:
            self.__dict__ = params

    def returnArray(self):
        return [self.mean_absolute_differencing_transaction_timestamps,
                self.mean_absolute_differencing_transaction_amount,
                self.median_longitude, self.median_latitude, self.median_target_ip, self.median_dest_ip,
                self.label]

    def getMeanAbsoluteDifferencingTransactionTimestamps(self):
        return self.mean_absolute_differencing_transaction_timestamps

    def getMeanAbsoluteDifferencingTransactionAmount(self):
        return self.mean_absolute_differencing_transaction_amount

    def getMedianLongitude(self):
        return self.median_longitude

    def getMedianLatitude(self):
        return self.median_latitude

    def getMedianTargetIP(self):
        return self.median_target_ip

    def getMedianDestIP(self):
        return self.median_dest_ip

    def getLabel(self):
        return self.label

    def to_row(self):
        return tuple(self.__dict__.values())

    @staticmethod
    def from_row(x):
        return PreparedSession(x)
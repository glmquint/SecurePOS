class PreparedSession:

    def __init__(self, params):
        if type(params) is not dict:  # this if i create a preparedSession from a list
            self.__mean_absolute_differencing_transaction_timestamps = params[0]
            self.__mean_absolute_differencing_transaction_amount = params[1]
            self.__median_longitude = params[2]
            self.__median_latitude = params[3]
            self.__median_target_ip = params[4]
            self.__median_dest_ip = params[5]
            self.__label = params[6]
        else:
            self.__dict__ = params

    def returnArray(self):
        return [self.__mean_absolute_differencing_transaction_timestamps,
                self.__mean_absolute_differencing_transaction_amount,
                self.__median_longitude, self.__median_latitude, self.__median_target_ip, self.__median_dest_ip,
                self.__label]

    def getMeanAbsoluteDifferencingTransactionTimestamps(self):
        return self.__mean_absolute_differencing_transaction_timestamps

    def getMeanAbsoluteDifferencingTransactionAmount(self):
        return self.__mean_absolute_differencing_transaction_amount

    def getMedianLongitude(self):
        return self.__median_longitude

    def getMedianLatitude(self):
        return self.__median_latitude

    def getMedianTargetIP(self):
        return self.__median_target_ip

    def getMedianDestIP(self):
        return self.__median_dest_ip

    def getLabel(self):
        return self.__label

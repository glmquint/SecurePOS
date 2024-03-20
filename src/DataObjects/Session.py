import json
from dataclasses import dataclass

from src.DataObjects.Feature import MeanAbsDiffTransaction, MeanAbsDiffTransactionAmount, MedianLongitudeLatitude, \
    MedianTargetIP, MedianDestIP, Feature, AttackRiskLabel
from src.DataObjects.Record import Record


class Session:
    pass
class RawSession(Session):
    records : [Record]
    def __init__(self, **kwargs):
        self.records = kwargs.get("records", [])
    def to_json(self):
        #return str([record.__repr__() for record in self.records])
        if not self.records or len(self.records) == 0:
            return {"records": []}
        return {"records": [Record.to_json(record) for record in self.records]}

class PreparedSession(Session):

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
            self.mean_abs_diff_transaction         : int    = params.get("mean_abs_diff_transaction", None)
            self.mean_abs_diff_transaction_amount  : int    = params.get("mean_abs_diff_transaction_amount", None)
            self.median_longitude                  : float  = params.get("median_longitude", None)
            self.median_latitude                   : float  = params.get("median_latitude", None)
            self.median_target_ip                  : int    = params.get("median_target_ip", None)
            self.median_dest_ip                    : int    = params.get("median_dest_ip", None)
            self.label                             : str    = params.get("attack_risk_label", None)

    def to_json(self):
        return {'mean_abs_diff_transaction': self.mean_abs_diff_transaction,
                'mean_abs_diff_transaction_amount': self.mean_abs_diff_transaction_amount,
                'median_longitude' : self.median_longitude,
                'median_latitude' : self.median_latitude,
                'median_target_ip': self.median_target_ip,
                'median_dest_ip': self.median_dest_ip,
                'label': self.label}
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
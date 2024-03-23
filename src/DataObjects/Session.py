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
    '''
    CREATE TABLE PreparedSessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT,
        mean_abs_diff_transaction REAL,
        mean_abs_diff_transaction_amount REAL,
        median_longitude REAL,
        median_latitude REAL,
        median_target_ip INTEGER,
        median_dest_ip INTEGER,
        label TEXT
    )
    '''

    def __init__(self, **kwargs):
        self.uuid                              : str    = kwargs.get("uuid", None)
        self.mean_abs_diff_transaction         : int    = kwargs.get("mean_abs_diff_transaction", None)
        self.mean_abs_diff_transaction_amount  : int    = kwargs.get("mean_abs_diff_transaction_amount", None)
        self.median_longitude                  : float  = kwargs.get("median_longitude", None)
        self.median_latitude                   : float  = kwargs.get("median_latitude", None)
        self.median_target_ip                  : int    = kwargs.get("median_target_ip", None)
        self.median_dest_ip                    : int    = kwargs.get("median_dest_ip", None)
        self.label                             : str    = kwargs.get("label", None)

    def to_json(self):
        return {'uuid': self.uuid,
                'mean_abs_diff_transaction': self.mean_abs_diff_transaction,
                'mean_abs_diff_transaction_amount': self.mean_abs_diff_transaction_amount,
                'median_longitude' : self.median_longitude,
                'median_latitude' : self.median_latitude,
                'median_target_ip': self.median_target_ip,
                'median_dest_ip': self.median_dest_ip,
                'label': self.label}
    def returnArray(self):
        return [self.uuid,
                self.mean_abs_diff_transaction,
                self.mean_abs_diff_transaction_amount,
                self.median_longitude, self.median_latitude, self.median_target_ip, self.median_dest_ip,
                self.label] # app logic heavily depends on label being last

    def getUuid(self):
        return self.uuid

    def getMeanAbsoluteDifferencingTransactionTimestamps(self):
        return self.mean_abs_diff_transaction

    def getMeanAbsoluteDifferencingTransactionAmount(self):
        return self.mean_abs_diff_transaction_amount

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
        return PreparedSession(**x)
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

    def __init__(self, **kwargs):
        self.mean_abs_diff_transaction         : int    = kwargs.get("mean_abs_diff_transaction", None)
        self.mean_abs_diff_transaction_amount  : int    = kwargs.get("mean_abs_diff_transaction_amount", None)
        self.median_longitude                  : float  = kwargs.get("median_longitude", None)
        self.median_latitude                   : float  = kwargs.get("median_latitude", None)
        self.median_target_ip                  : int    = kwargs.get("median_target_ip", None)
        self.median_dest_ip                    : int    = kwargs.get("median_dest_ip", None)
        self.label                             : str    = kwargs.get("attack_risk_label", None)

    def to_json(self):
        return {'mean_absolute_differencing_transaction_timestamps': self.mean_abs_diff_transaction,
                'mean_absolute_differencing_transaction_amount': self.mean_abs_diff_transaction_amount,
                'median_longitude' : self.median_longitude,
                'median_latitude' : self.median_latitude,
                'median_target_ip': self.median_target_ip,
                'median_dest_ip': self.median_dest_ip,
                'label': self.label}
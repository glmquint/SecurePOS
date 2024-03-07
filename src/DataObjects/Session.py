import json
from dataclasses import dataclass

from src.DataObjects.Feature import MeanAbsDiffTransaction, MeanAbsDiffTransactionAmount, MedianLongitudeLatitude, \
    MedianTargetIP, MedianDestIP, Feature
from src.DataObjects.Record import Record


class Session:
    pass
class RawSession(Session):
    records : [Record]
    def __init__(self, **kwargs):
        self.records = [Record(**x) for x in kwargs.get("records", [])]
    def to_json(self):
        #return str([record.__repr__() for record in self.records])
        if not self.records or len(self.records) == 0:
            return {"records": []}
        return {"records": [record.to_json() for record in self.records]}

@dataclass
class PreparedSession(Session):
    features: [Feature]

    def __init__(self, **kwargs):
        self.features = []
        self.features.append(MeanAbsDiffTransaction(**kwargs.get("mean_abs_diff_transaction", {})))
        self.features.append(MeanAbsDiffTransactionAmount(**kwargs.get("mean_abs_diff_transaction_amount", {})))
        self.features.append(MedianLongitudeLatitude(**kwargs.get("median_longitude_latitude", {})))
        self.features.append(MedianTargetIP(**kwargs.get("median_target_ip", {})))
        self.features.append(MedianDestIP(**kwargs.get("median_dest_ip", {})))

    def to_json(self):
        if not self.features or len(self.features) == 0:
            return {"features": []}
        return {"features": [feature.to_json() for feature in self.features]}
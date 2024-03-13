from dataclasses import dataclass
from datetime import datetime


class Record:
    def __init__(self, **kwargs):
        self.uuid:str = kwargs.get('uuid', '')

    def to_json(self):
        return {"uuid": self.uuid}

    def to_row(self):
        return tuple([self.uuid, str(type(self)), self.to_json()])

    @staticmethod
    def from_row(**row):
        row_type = row.get('type', None)
        # TODO: check if this is the right way to do this
        if row_type == LocalizationSysRecord:
            return LocalizationSysRecord(**row.get('data', {}))
        if row_type == NetworkMonitorRecord:
            return NetworkMonitorRecord(**row.get('data', {}))
        if row_type == TransactionCloudRecord:
            return TransactionCloudRecord(**row.get('data', {}))
        return Record(**row.get('data', {}))

class LocalizationSysRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location_latitude: float = kwargs.get("location_latitude", 0.0)
        self.location_longitude: float = kwargs.get("location_longitude", 0.0)
    def to_json(self):
        data = {"location_latitude":self.location_latitude,
                "location_longitude":self.location_longitude}
        data.update(super().to_json())
        return data
    def isMissingSample(self):
        return self.location_latitude == 0.0 or self.location_longitude == 0.0


class NetworkMonitorRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_ip: str = kwargs.get("target_ip", "")
        self.dest_ip: str = kwargs.get("dest_ip", "")
    def to_json(self):
        data = {"target_ip":self.target_ip,
                "dest_ip":self.dest_ip}
        data.update(super().to_json())
        return data
    def isMissingSample(self):
        return self.target_ip == '' or self.dest_ip == ''


class TransactionCloudRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp: [int] = kwargs.get("timestamp", [])
        self.amount: [int] = kwargs.get("amount", [])
    def to_json(self):
        data = {"timestamp":self.timestamp,
                "amount":self.amount}
        data.update(super().to_json())
        return data
    def isMissingSample(self):
        return len(self.timestamp) == 0 or len(self.amount) == 0

class Label(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label: str = kwargs.get("label", '')
    def to_json(self):
        data = {"label":self.label}
        data.update(super().to_json())
        return data
    def isMissingSample(self):
        return self.label == ''

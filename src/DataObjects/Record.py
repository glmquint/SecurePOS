from dataclasses import dataclass
from datetime import datetime


class Record:
    def __init__(self, **kwargs):
        self.uuid:str = kwargs.get('uuid', '')

    def to_json(self):
        return {'uuid': self.uuid}

class LocalizationSysRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location_latitude: float = kwargs.get("location_latitude", 0.0)
        self.location_longitude: float = kwargs.get("location_longitude", 0.0)
    def to_json(self):
        data = {'location_latitude':self.location_latitude,
                'location_longitude':self.location_longitude}
        data.update(super().to_json())
        return data


class NetworkMonitorRecord(Record):
    def __init__(self, **kwargs):
        super()
        self.target_ip: str = kwargs.get("target_ip", "")
        self.dest_ip: str = kwargs.get("dest_ip", "")
    def to_json(self):
        data = {'target_ip':self.target_ip,
                'dest_ip':self.dest_ip}
        data.update(super().to_json())
        return data


class TransactionCloudRecord(Record):
    def __init__(self, **kwargs):
        super()
        self.timestamp: [int] = kwargs.get("timestamp", [])
        self.amount: [int] = kwargs.get("amount", [])
    def to_json(self):
        data = {'timestamp':self.timestamp,
                'amount':self.amount}
        data.update(super().to_json())
        return data

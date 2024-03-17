import json
from dataclasses import dataclass
from datetime import datetime


class Record:
    def __init__(self, **kwargs):
        self.uuid:str = kwargs.get('uuid', None)

    def to_json(self):
        return {"uuid": self.uuid, "objtype": str(type(self)), "data": self.to_json()}

    def to_row(self):
        return tuple([json.dumps(x) if type(x) is dict else x for x in Record.to_json(self).values()])

    @staticmethod
    def from_row(uuid='', objtype='', data='{}'):
        json_data = json.loads(data) if type(data) is str else data
        json_data.update({'uuid':uuid})
        if objtype == str(LocalizationSysRecord):
            return LocalizationSysRecord(**json_data)
        if objtype == str(NetworkMonitorRecord):
            return NetworkMonitorRecord(**json_data)
        if objtype == str(TransactionCloudRecord):
            return TransactionCloudRecord(**json_data)
        return Record(**json_data)

    def getMissingSamples(self):
        return [k for k, v in self.__dict__.items() if v is None]

class LocalizationSysRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location_latitude: float = kwargs.get("location_latitude", None)
        self.location_longitude: float = kwargs.get("location_longitude", None)
    def to_json(self):
        data = {"location_latitude":self.location_latitude,
                "location_longitude":self.location_longitude}
        return data

class NetworkMonitorRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_ip: str = kwargs.get("target_ip", None)
        self.dest_ip: str = kwargs.get("dest_ip", None)
    def to_json(self):
        data = {"target_ip":self.target_ip,
                "dest_ip":self.dest_ip}
        return data

class TransactionCloudRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp: [int] = kwargs.get("timestamp", None)
        self.amount: [int] = kwargs.get("amount", None)
    def to_json(self):
        data = {"timestamp":self.timestamp,
                "amount":self.amount}
        return data

class Label(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label: str = kwargs.get("label", None)
    def to_json(self):
        data = {"label":self.label}
        return data

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

    def clamp(self, key, value):
        raise Exception(f"Cannot clamp: {key} not in {self.__dict__}")

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
        if objtype == str(Label):
            return Label(**json_data)
        else:
            raise Exception("Cannot deserialize: unknown objtype")
        return Record(**json_data)

    def getMissingSamples(self):
        return [k for k, v in self.__dict__.items() if v is None]

min_lat = -90
max_lat = 90
min_long = -180
max_long = 180
class LocalizationSysRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location_latitude: float = kwargs.get("location_latitude", None)
        self.location_longitude: float = kwargs.get("location_longitude", None)

    def to_json(self):
        data = {"location_latitude":self.location_latitude,
                "location_longitude":self.location_longitude}
        return data
    def getOutliers(self):
        return {k: v for k, v in self.__dict__.items() if k == 'location_latitude' and (v < min_lat or v > max_lat) or k == 'location_longitude' and (v < min_long or v > max_long)}
    def clamp(self, key, value):
        if key == 'location_latitude':
            self.__dict__[key] = min(max_lat, max(min_lat, value))
        if key == 'location_longitude':
            self.__dict__[key] = min(max_long, max(min_long, value))

class NetworkMonitorRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_ip: str = kwargs.get("target_ip", None)
        self.dest_ip: str = kwargs.get("dest_ip", None)
    def to_json(self):
        data = {"target_ip":self.target_ip,
                "dest_ip":self.dest_ip}
        return data
    def getOutliers(self):
        return {k: v for k, v in self.__dict__.items() if not self.isValidIP(v)}
    def isValidIP(self, ip):
        return ip.count('.') == 3 and all([0 <= int(x) <= 255 for x in ip.split('.')])
    def clamp(self, key, value):
        if key == 'target_ip' or key == 'dest_ip':
            self.__dict__[key] = '.'.join([str(min(255, max(0, int(x)))) for x in value.split('.')])

class TransactionCloudRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp: [int] = kwargs.get("timestamp", None)
        self.amount: [int] = kwargs.get("amount", None)
    def to_json(self):
        data = {"timestamp":self.timestamp,
                "amount":self.amount}
        return data
    def getOutliers(self):
        return {'timestamp':[i for i, x in enumerate(self.timestamp) if x is None],
                'amount':[i for i, x in enumerate(self.amount) if x is None or x < 0]}
    def clamp(self, key, value):
        for index in value:
            if index < 0 or type(index) is not int:
                return
            if key not in ['timestamp', 'amount']:
                return
            # we prefer the last known sample to interpolate, but if none is found we search in the future
            up_to_i = set([i for i in range(index) if i not in self.getOutliers()[key]]) # all valid indexes up to 'index' (not included)
            if len(up_to_i) == 0:
                down_to_i = set([i for i in range(len(self.__dict__[key]), index, -1) if i not in self.getOutliers()[key]]) # all valid indexes from 'index' (not included) up to the last one (included)
                if len(down_to_i) == 0:
                    raise Exception(f"Cannot interpolate: no valid index found in timeseries {key}")
                alternative_idx = min(down_to_i)
            else:
                alternative_idx = max(up_to_i)
            self.__dict__[key][index] = self.__dict__[key][alternative_idx]


class Label(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label: str = kwargs.get("label", None)
    def to_json(self):
        data = {"label":self.label}
        return data
    def getOutliers(self):
        return {k:v for k, v in self.__dict__.items() if v not in ['normal', 'moderate', 'high']}
    def clamp(self, key, value):
        if key != 'label':
            return
        value = value.lower()
        if value in ['normal', 'moderate', 'high']:
            self.__dict__[key] = value
        else:
            raise Exception(f"Cannot clamp: {value} not in ['normal', 'moderate', 'high']")

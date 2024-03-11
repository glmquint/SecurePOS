import json


class RecordOld:
    def __init__(self, **kwargs) -> None:
        self.uuid:str = kwargs.get("uuid", "")
        self.timestamp:[int] = kwargs.get("timestamp", [])
        self.amount:[int] = kwargs.get("amount", [])
        self.target_ip:str = kwargs.get("target_ip", "")
        self.dest_ip:str = kwargs.get("dest_ip", "")
        self.location_latitude:float = kwargs.get("location_latitude", 0.0)
        self.location_longitude:float = kwargs.get("location_longitude", 0.0)

    def isMissingSample(self) -> bool:
        return (self.uuid == "" or self.timestamp == "" or self.amount == 0 or self.target_ip == "" or self.dest_ip == "" or self.location_latitude == 0.0 or self.location_longitude == 0.0)

    def to_json(self):
        return {
            "uuid": self.uuid,
            "timestamp": str(self.timestamp),
            "amount": str(self.amount),
            "target_ip": self.target_ip,
            "dest_ip": self.dest_ip,
            "location_latitude": self.location_latitude,
            "location_longitude": self.location_longitude
        }

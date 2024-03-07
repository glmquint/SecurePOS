import json


class Record:
    def __init__(self, **kwargs) -> None:
        self.device_src:str = kwargs.get("device_src", "")
        self.timestamp:str = kwargs.get("timestamp", "")
        self.amount:int = kwargs.get("amount", 0)
        self.target_ip:str = kwargs.get("target_ip", "")
        self.dest_ip:str = kwargs.get("dest_ip", "")
        self.location_latitude:float = kwargs.get("location_latitude", 0.0)
        self.location_longitude:float = kwargs.get("location_longitude", 0.0)

    def isMissingSample(self) -> bool:
        return (self.device_src == "" or self.timestamp == "" or self.amount == 0 or self.target_ip == "" or self.dest_ip == "" or self.location_latitude == 0.0 or self.location_longitude == 0.0)

    def to_json(self):
        return self.__dict__

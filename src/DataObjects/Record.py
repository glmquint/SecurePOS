class Record:
    def __init__(self, device_src:str="", timestamp:str="", amount:int=0, target_ip:str="", dest_ip:str="", location_latitude:float=0.0, location_longitude:float=0.0) -> None:
        self.device_src:str = device_src
        self.timestamp:str = timestamp
        self.amount:int = amount
        self.target_ip:str = target_ip
        self.dest_ip:str = dest_ip
        self.location_latitude:float = location_latitude
        self.location_longitude:float = location_longitude

    def isMissingSample(self) -> bool:
        return (self.device_src == "" or self.timestamp == "" or self.amount == 0 or self.target_ip == "" or self.dest_ip == "" or self.location_latitude == 0.0 or self.location_longitude == 0.0)
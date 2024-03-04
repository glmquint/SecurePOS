from src.DataObjects.Sample import Sample


class Record:
    def __init__(self):
        self.device_src: str = ""
        self.timestamp: str = ""
        self.amount: int = 0
        self.target_ip: str = ""
        self.dest_ip: str = ""
        self.location_latitude: float = 0.0
        self.location_longitude: float = 0.0
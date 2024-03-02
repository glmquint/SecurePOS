from dataclasses import dataclass
from datetime import datetime


@dataclass
class Sample:
    device_src = ""

class LocalizationSysSample(Sample):
    location_latitude:float = 0.0
    location_longitude:float = 0.0
class NetworkMonitorSample(Sample):
    target_ip:str = ""
    dest_ip:str = ""

class TransactionCloudSample(Sample):
    timestamp:datetime = None
    amount:int = 0

from dataclasses import dataclass

from src.DataObjects.Feature import MeanAbsDiffTransaction, MeanAbsDiffTransactionAmount, MedianLongitudeLatitude, \
    MedianTargetIP, MedianDestIP
from src.DataObjects.Record import Record


class Session:
    pass

class RawSession(Session):
    records = [Record]
@dataclass
class PreparedSession(Session):
    mean_abs_diff_transaction:MeanAbsDiffTransaction = None
    mean_abs_diff_transaction_amount:MeanAbsDiffTransactionAmount = None
    median_longitude_latitude:MedianLongitudeLatitude = None
    median_target_ip:MedianTargetIP = None
    median_dest_ip:MedianDestIP = None

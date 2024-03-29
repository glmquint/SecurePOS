from src.DataObjects.Record import Record
from typing import Optional

class Session:
    """
    A base class used to represent a session in the development system.

    This class is intended to be subclassed and does not provide any implementation.
    """
    pass


class RawSession(Session):
    """
    A subclass of the Session class used to represent a raw session in the development system.

    Attributes
    ----------
    records : list[Record]
        The records of the session.

    Methods
    -------
    __init__(self, **kwargs)
        Initializes the RawSession class with a list of records.
    to_json(self)
        Converts the RawSession instance to a JSON-compatible dictionary.
    """
    # class implementation...
    records: [Record]

    def __init__(self, **kwargs):
        self.records = kwargs.get("records", [])

    def to_json(self):
        # return str([record.__repr__() for record in self.records])
        if not self.records or len(self.records) == 0:
            return {"records": []}
        return {"records": [Record.to_json(record) for record in self.records]}


class PreparedSession(Session):
    """
    A subclass of the Session class used to represent a prepared session in the development system.

    Attributes
    ----------
    uuid : str
        The unique identifier of the session.
    mean_abs_diff_transaction : int
        The mean absolute difference of transactions.
    mean_abs_diff_transaction_amount : int
        The mean absolute difference of transaction amounts.
    median_longitude : float
        The median longitude of the session.
    median_latitude : float
        The median latitude of the session.
    median_target_ip : int
        The median target IP address of the session.
    median_dest_ip : int
        The median destination IP address of the session.
    label : str
        The label of the session.

    Methods
    -------
    __init__(self, **kwargs)
        Initializes the PreparedSession class with a unique identifier, mean absolute differences, medians, and a label.
    to_json(self)
        Converts the PreparedSession instance to a JSON-compatible dictionary.
    returnArray(self)
        Returns the attributes of the PreparedSession instance as a list.
    getUuid(self)
        Returns the unique identifier of the PreparedSession instance.
    getMeanAbsoluteDifferencingTransactionTimestamps(self)
        Returns the mean absolute difference of transactions of the PreparedSession instance.
    getMeanAbsoluteDifferencingTransactionAmount(self)
        Returns the mean absolute difference of transaction amounts of the PreparedSession instance.
    getMedianLongitude(self)
        Returns the median longitude of the PreparedSession instance.
    getMedianLatitude(self)
        Returns the median latitude of the PreparedSession instance.
    getMedianTargetIP(self)
        Returns the median target IP address of the PreparedSession instance.
    getMedianDestIP(self)
        Returns the median destination IP address of the PreparedSession instance.
    getLabel(self)
        Returns the label of the PreparedSession instance.
    to_row(self)
        Converts the PreparedSession instance to a tuple.
    from_row(x)
        Deserializes a row into a PreparedSession instance.
    """
    # class implementation...
    '''
    CREATE TABLE PreparedSessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT,
        mean_abs_diff_transaction REAL,
        mean_abs_diff_transaction_amount REAL,
        median_longitude REAL,
        median_latitude REAL,
        median_target_ip INTEGER,
        median_dest_ip INTEGER,
        label TEXT
    )
    '''

    def __init__(self, **kwargs):
        self.uuid: Optional[str] = kwargs.get("uuid", None)
        self.mean_abs_diff_transaction: Optional[int] = kwargs.get(
            "mean_abs_diff_transaction", None)
        self.mean_abs_diff_transaction_amount: Optional[int] = kwargs.get(
            "mean_abs_diff_transaction_amount", None)
        self.median_longitude: Optional[float] = kwargs.get("median_longitude", None)
        self.median_latitude: Optional[float] = kwargs.get("median_latitude", None)
        self.median_target_ip: Optional[int] = int(kwargs.get("median_target_ip", None))
        self.median_dest_ip: Optional[int] = int(kwargs.get("median_dest_ip", None))
        self.label: Optional[str] = kwargs.get("label", None)

    def to_json(self):
        return {
            'uuid': self.uuid,
            'mean_abs_diff_transaction': self.mean_abs_diff_transaction,
            'mean_abs_diff_transaction_amount': self.mean_abs_diff_transaction_amount,
            'median_longitude': self.median_longitude,
            'median_latitude': self.median_latitude,
            'median_target_ip': self.median_target_ip,
            'median_dest_ip': self.median_dest_ip,
            'label': self.label}

    def return_array(self):
        return [
            self.uuid,
            self.mean_abs_diff_transaction,
            self.mean_abs_diff_transaction_amount,
            self.median_longitude,
            self.median_latitude,
            self.median_target_ip,
            self.median_dest_ip,
            self.label]  # app logic heavily depends on label being last

    def get_uuid(self):
        return self.uuid

    def get_mean_absolute_differencing_transaction_timestamps(self):
        return self.mean_abs_diff_transaction

    def get_mean_absolute_differencing_transaction_amount(self):
        return self.mean_abs_diff_transaction_amount

    def get_median_longitude(self):
        return self.median_longitude

    def get_median_latitude(self):
        return self.median_latitude

    def get_median_target_ip(self):
        return self.median_target_ip

    def get_median_dest_ip(self):
        return self.median_dest_ip

    def get_label(self):
        return self.label

    def to_row(self):
        return tuple(self.__dict__.values())

    @staticmethod
    def from_row(x):
        return PreparedSession(**x)

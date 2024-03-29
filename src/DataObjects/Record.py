import json
from typing import Optional

class Record:
    """
    A class used to represent a record in the development system.

    Attributes
    ----------
    uuid : str
        The unique identifier of the record.

    Methods
    -------
    __init__(self, **kwargs)
        Initializes the Record class with a unique identifier.
    to_json(self)
        Converts the Record instance to a JSON-compatible dictionary.
    to_row(self)
        Converts the Record instance to a tuple.
    clamp(self, key, value)
        Raises an exception if the key is not in the instance's dictionary.
    from_row(uuid='', objtype='', data='{}')
        Deserializes a row into a Record instance or a subclass instance based on the objtype.
    get_missing_samples(self)
        Returns a list of keys for which the instance's dictionary has None values.
    """
    # class implementation...class Record:
    def __init__(self, **kwargs):
        self.uuid: Optional[str] = kwargs.get('uuid', None)

    def to_json(self):
        return {
            "uuid": self.uuid,
            "objtype": str(
                type(self)),
            "data": self.to_json()}

    def to_row(self):
        return tuple([json.dumps(x) if isinstance(x, dict)
                     else x for x in Record.to_json(self).values()])

    def clamp(self, key, value):
        raise Exception(f"Cannot clamp: {key} not in {self.__dict__}")

    @staticmethod
    def from_row(uuid='', objtype='', data='{}'):
        json_data = json.loads(data) if isinstance(data, str) else data
        json_data.update({'uuid': uuid})
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

    def get_missing_samples(self):
        return [k for k, v in self.__dict__.items() if v is None]


min_lat = -90
max_lat = 90
min_long = -180
max_long = 180


class LocalizationSysRecord(Record):
    """
    A subclass of the Record class used to represent a localization system record in the development system.

    Attributes
    ----------
    location_latitude : float
        The latitude of the location.
    location_longitude : float
        The longitude of the location.

    Methods
    -------
    __init__(self, **kwargs)
        Initializes the LocalizationSysRecord class with a unique identifier, latitude, and longitude.
    to_json(self)
        Converts the LocalizationSysRecord instance to a JSON-compatible dictionary.
    get_outliers(self)
        Returns a dictionary of attributes that are outside the valid range.
    clamp(self, key, value)
        Clamps the value of the specified attribute to its valid range.
    """
    # class implementation...class LocalizationSysRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.location_latitude: Optional[float] = kwargs.get("location_latitude", None)
        self.location_longitude: Optional[float] = kwargs.get("location_longitude", None)

    def to_json(self):
        data = {"uuid": self.uuid, "location_latitude": self.location_latitude,
                "location_longitude": self.location_longitude}
        return data

    def get_outliers(self):
        return {
            k: v for k,
            v in self.__dict__.items() if k == 'location_latitude' and (
                v < min_lat or v > max_lat) or k == 'location_longitude' and (
                v < min_long or v > max_long)}

    def clamp(self, key, value):
        if key == 'location_latitude':
            self.__dict__[key] = min(max_lat, max(min_lat, value))
        if key == 'location_longitude':
            self.__dict__[key] = min(max_long, max(min_long, value))


class NetworkMonitorRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_ip: Optional[str] = kwargs.get("target_ip", None)
        self.dest_ip: Optional[str] = kwargs.get("dest_ip", None)

    def to_json(self):
        data = {"uuid": self.uuid, "target_ip": self.target_ip,
                "dest_ip": self.dest_ip}
        return data

    def get_outliers(self):
        return {k: v for k, v in self.__dict__.items() if not self.is_valid_ip(v)}

    def is_valid_ip(self, ip):
        return ip.count('.') == 3 and all(
            [0 <= int(x) <= 255 for x in ip.split('.')])

    def clamp(self, key, value):
        if key == 'target_ip' or key == 'dest_ip':
            self.__dict__[key] = '.'.join(
                [str(min(255, max(0, int(x)))) for x in value.split('.')])


class TransactionCloudRecord(Record):
    """
    A subclass of the Record class used to represent a transaction cloud record in the development system.

    Attributes
    ----------
    timestamp : list[int]
        The timestamps of the transactions.
    amount : list[int]
        The amounts of the transactions.

    Methods
    -------
    __init__(self, **kwargs)
        Initializes the TransactionCloudRecord class with a unique identifier, timestamps, and amounts.
    to_json(self)
        Converts the TransactionCloudRecord instance to a JSON-compatible dictionary.
    get_outliers(self)
        Returns a dictionary of attributes that are outside the valid range.
    clamp(self, key, value)
        Clamps the value of the specified attribute to its valid range.
    """
    # class implementation...class TransactionCloudRecord(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp: [int] = kwargs.get("timestamp", None)
        self.amount: [int] = kwargs.get("amount", None)

    def to_json(self):
        data = {"uuid": self.uuid, "timestamp": self.timestamp,
                "amount": self.amount}
        return data

    def get_outliers(self):
        return {
            'timestamp': [
                i for i, x in enumerate(
                    self.timestamp) if x is None], 'amount': [
                i for i, x in enumerate(
                    self.amount) if x is None or x < 0]}

    def clamp(self, key, value):
        for index in value:
            if index < 0 or not isinstance(index, int):
                return
            if key not in ['timestamp', 'amount']:
                return
            # we prefer the last known sample to interpolate, but if none is
            # found we search in the future
            # all valid indexes up to 'index' (not included)
            up_to_i = set(
                [i for i in range(index) if i not in self.get_outliers()[key]])
            if len(up_to_i) == 0:
                # all valid indexes from 'index' (not included) up to the last
                # one (included)
                down_to_i = set([i for i in range(
                    len(self.__dict__[key]), index, -1) if i not in self.get_outliers()[key]])
                if len(down_to_i) == 0:
                    raise Exception(
                        f"Cannot interpolate: no valid index found in timeseries {key}")
                alternative_idx = min(down_to_i)
            else:
                alternative_idx = max(up_to_i)
            self.__dict__[key][index] = self.__dict__[key][alternative_idx]


class Label(Record):
    """
    A subclass of the Record class used to represent a label in the development system.

    Attributes
    ----------
    label : str
        The label of the record.

    Methods
    -------
    __init__(self, **kwargs)
        Initializes the Label class with a unique identifier and a label.
    to_row(self)
        Converts the Label instance to a tuple.
    from_row(self)
        Deserializes a row into a Label instance.
    to_json(self)
        Converts the Label instance to a JSON-compatible dictionary.
    get_outliers(self)
        Returns a dictionary of attributes that are outside the valid range.
    clamp(self, key, value)
        Clamps the value of the specified attribute to its valid range.
    """
    # class implementation...class Label(Record):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label: Optional[str] = kwargs.get("label", None)

    @staticmethod
    def to_row(obj):
        return tuple([obj.label, obj.uuid])

    @staticmethod
    def from_row(obj):
        return Label(uuid=obj["uuid"], label=obj["label"])

    def to_json(self):
        data = {"uuid": self.uuid, "label": self.label}
        return data

    def get_outliers(self):
        return {
            k: v for k,
            v in self.__dict__.items() if v not in [
                'normal',
                'moderate',
                'high']}

    def clamp(self, key, value):
        if key != 'label':
            return
        value = value.lower()
        if value in ['normal', 'moderate', 'high']:
            self.__dict__[key] = value
        else:
            raise Exception(
                f"Cannot clamp: {value} not in ['normal', 'moderate', 'high']")

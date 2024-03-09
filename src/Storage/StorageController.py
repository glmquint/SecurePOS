from threading import Event

from src.Storage.DBConnector import DBConnector
from src.util import log


class StorageController:
    DBConnector = None
    type = None

    def __init__(self, dbConfig, type):
        self.type = type
        self.DBConnector = DBConnector(dbConfig)
        self.count_updated = Event()
        self.count_updated.set()

    def save(self, obj):
        if type(obj) is not self.type:
            raise Exception(f'Invalid type, expected {self.type} got {type(obj)}')
        row = [tuple(obj.__dict__.values())]
        try:
            self.DBConnector.insert(row)
            self.count_updated.set()
        except Exception as e:
            print(__name__, e)
            return False
        return True

    def remove_all(self):
        try:
            self.DBConnector.remove()
            self.count_updated.set()
        except Exception as e:
            print(e)
            return False
        return True

    def retrieve_all(self):
        data_elem = self.DBConnector.retrieve()
        return [self.type(**elem) for elem in data_elem]

    def count(self) -> int:
        self.count_updated.wait()
        self.count_updated.clear()
        return self.DBConnector.count()

    def delete_by_column(self, column, value) -> bool:
        try:
            self.DBConnector.delete_by_column(column, value)
            self.count_updated.set()
        except Exception as e:
            print(e)
            return False
        return True
from src.Storage.DBConnector import DBConnector
from src.util import log


class StorageController:
    DBConnector = None
    type = None

    def __init__(self, dbConfig, type):
        self.type = type
        self.DBConnector = DBConnector(dbConfig)

    @log
    def save(self, obj):
        if type(obj) is not self.type:
            raise Exception(f'Invalid type, expected {self.type} got {type(obj)}')
        row = [tuple(obj.__dict__.values())]
        try:
            self.DBConnector.insert(row)
        except Exception as e:
            print(e)
            return False
        return True

    @log
    def remove_all(self):
        try:
            self.DBConnector.remove()
        except Exception as e:
            print(e)
            return False
        return True

    @log
    def retrieve_all(self):
        data_elem = self.DBConnector.retrieve()
        return [self.type(elem) for elem in data_elem]

    @log
    def count(self):
        return self.DBConnector.count()

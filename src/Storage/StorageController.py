from threading import Event

from src.Storage.DBConnector import DBConnector
from src.util import log


class StorageController:

    def __init__(self, dbConfig, type):
        self.type = type
        self.DBConnector = DBConnector(name = dbConfig['name'], table_name = dbConfig['table_name'])
        self.count_updated = Event()
        self.count_updated.set()

    def save(self, obj):
        if not issubclass(type(obj), self.type):
            raise Exception(f'Invalid type, expected {self.type} got {type(obj)}')
        row = [obj.to_row()]
        try:
            self.DBConnector.insert(row)
            self.count_updated.set()
        except Exception as e:
            print(__name__, e)
            return False
        return True

    def wait_count_updated(self):
        self.count_updated.wait()
        self.count_updated.clear()
        return

    def remove_all(self):
        try:
            self.DBConnector.remove()
            self.count_updated.set()
        except Exception as e:
            print(e)
            return False
        return True

    def retrieve_all(self) -> [type]:
        self.wait_count_updated()
        return [self.type.from_row(x) for x in self.DBConnector.retrieve()]

    def count(self) -> int:
        self.wait_count_updated()
        return self.DBConnector.count()

    def remove_by_column(self, column, value) -> bool:
        try:
            self.DBConnector.delete_by_column(column, value)
            self.count_updated.set()
        except Exception as e:
            print(e)
            return False
        return True

    def executeQuery(self, param):
        cursor = self.DBConnector.connection.cursor()
        cursor.execute(param)
        return cursor.fetchall()

    def retrieve_by_column(self, param, value):
        try:
            return self.DBConnector.retrieve_by_column(param, value)
        except Exception as e:
            print(e)
        return []


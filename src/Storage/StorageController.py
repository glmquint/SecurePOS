from threading import Event, Thread
from time import sleep

from src.Storage.DBConnector import DBConnector
from src.DataObjects.Session import PreparedSession
from src.util import log, monitorPerformance


class StorageController:
    DBConnector = None
    obj_type = None

    def __init__(self, dbConfig, obj_type, buffer_size=1):
        self.obj_type = obj_type
        self.DBConnector = DBConnector(name=dbConfig['name'], table_name=dbConfig['table_name'])
        self.count_updated = Event()
        self.count_updated.set()
        self.buffer_size = buffer_size
        self.buffer = []
        self.timeout_flush_thread = Thread(target=self.timeout_flush, daemon=True)
        self.timeout_flush_thread.start()


    @monitorPerformance(should_sample_after=False)
    def save(self, obj) -> bool:
        if not issubclass(type(obj), self.obj_type):
            raise Exception(f'Invalid type, expected {self.obj_type} got {type(obj)}')
        #row = [obj.to_row()]
        #todo fix this to be parametric
        row = [self.obj_type.to_row(obj)]
        self.buffer.extend(row)
        if len(self.buffer) >= self.buffer_size:
            return self.flush()
        return True

    def timeout_flush(self):
        while True:
            sleep(5)
            if len(self.buffer) > 0:
                self.flush()

    def flush(self) -> bool:
        try:
            self.DBConnector.insert(self.buffer)
            self.count_updated.set()
            self.buffer = []
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

    def retrieve_n(self, number:int,blocking=True) -> [type]:
        if blocking:
            self.wait_count_updated()
        try:
            result = [self.obj_type.from_row(x) for x in self.DBConnector.retrieve_n(number)]
        except Exception as e:
            print(e)
            with open("error.log", "a") as f:
                f.write(f"{e} ({__file__})\n")
            return []
        return result

    def remove_n(self,number:int):
        try:
            self.DBConnector.remove_n(number)
            self.count_updated.set()
        except Exception as e:
            print(e)
            with open("error.log", "a") as f:
                f.write(f"{e} ({__file__})\n")
            return False
        return True

    def retrieve_all(self, blocking=True) -> [type]:
        if blocking:
            self.wait_count_updated()
        return [self.obj_type.from_row(x) for x in self.DBConnector.retrieve()]

    def count(self, blocking=True) -> int:
        if blocking:
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

    def isNumberOfRecordsSufficient(self):
        self.wait_count_updated()
        return self.DBConnector.isNumberOfRecordsSufficient()

    def retrieve_by_column(self, param, value):
        try:
            return self.DBConnector.retrieve_by_column(param, value)
        except Exception as e:
            print(e)
        return []

from threading import Event, Thread
from time import sleep
from src.DataObjects.Record import Label
from src.Storage.DBConnector import DBConnector
from src.util import log, monitorPerformance


class StorageController:
    """
        This class is responsible for managing the storage of data in a database.
        It initializes the storage controller with a database configuration and an object type,
        and provides methods for various storage operations such as save, flush, remove, and retrieve.

        Attributes:
            DBConnector: An instance of the DBConnector class for database operations.
            obj_type: The type of the object that is being stored.
            buffer_size: The size of the buffer for storing objects before they are flushed to the database.
            buffer: A list that stores objects before they are flushed to the database.
            count_updated: An event that is set when the count of objects in the database is updated.
            timeout_flush_thread: A thread that flushes the buffer to the database every 5 seconds.

        Methods:
            save: Saves an object to the buffer and flushes the buffer to the database if it is full.
            timeout_flush: Flushes the buffer to the database every 5 seconds.
            flush: Flushes the buffer to the database.
            wait_count_updated: Waits until the count of objects in the database is updated.
            remove_all: Removes all objects from the database.
            remove_joined_labels: Removes a specified number of joined labels from the database.
            retrieve_n_labels: Retrieves a specified number of labels from the database.
            retrieve_n: Retrieves a specified number of objects from the database.
            remove_n: Removes a specified number of objects from the database.
            retrieve_all: Retrieves all objects from the database.
            count: Counts the number of objects in the database.
            remove_by_column: Removes objects from the database where a specified column has a specified value.
            isNumberOfRecordsSufficient: Checks if the number of records in the database is sufficient.
            retrieve_by_column: Retrieves objects from the database where a specified column has a specified value.
    """
    DBConnector = None
    obj_type = None

    def __init__(self, dbConfig, obj_type, buffer_size=1):
        self.obj_type = obj_type
        self.DBConnector = DBConnector(
            name=dbConfig['name'],
            table_name=dbConfig['table_name'])
        self.count_updated = Event()
        self.count_updated.set()
        self.buffer_size = buffer_size
        self.buffer = []
        self.timeout_flush_thread = Thread(
            target=self.timeout_flush, daemon=True)
        self.timeout_flush_thread.start()

    @log
    def save(self, obj) -> bool:
        if not issubclass(type(obj), self.obj_type):
            raise Exception(
                f'Invalid type, expected {self.obj_type} got {type(obj)}')
        # row = [obj.to_row()]
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

    def remove_joined_labels(self, number: int) -> [type]:
        try:
            self.DBConnector.remove_joined_labels(number)
            self.count_updated.set()
        except Exception as e:
            print(e)
            return False
        return True

    def retrieve_n_labels(self, number: int, blocking=True) -> [type]:
        if blocking:
            self.wait_count_updated()
        try:
            joined_result = self.DBConnector.retrieve_joined_labels(number)
            labels = []
            security_labels = []
            for x in joined_result:
                l1 = Label(label=x[1], uuid=x[2])
                l2 = Label(label=x[4], uuid=x[5])
                labels.append(l1)
                security_labels.append(l2)
            result = [labels, security_labels]
        except Exception as e:
            print(e)
            with open("error.log", "a") as f:
                f.write(f"{e} ({__file__})\n")
            return []
        return result

    def retrieve_n(self, number: int, blocking=True) -> [type]:
        if blocking:
            self.wait_count_updated()
        try:
            result = [self.obj_type.from_row(
                x) for x in self.DBConnector.retrieve_n(number)]
        except Exception as e:
            print(e)
            with open("error.log", "a") as f:
                f.write(f"{e} ({__file__})\n")
            return []
        return result

    def remove_n(self, number: int):
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

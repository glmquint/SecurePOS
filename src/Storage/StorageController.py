import json
from src.Storage.CSVConnector import CSVConnector
from src.DataObjects.ElasticitySample import ElasticitySample
from src.Storage.DBConnector import DBConnector


class StorageController:
    DBConnector = None
    type = None

    def __init__(self, config, type):
        self.type = type
        if type is ElasticitySample:
            self.CSVConnector = CSVConnector(config)
        else:
            self.DBConnector = DBConnector(config)

    def save(self, obj):
        if type(obj) is not self.type:
            raise Exception('Invalid type')
        try:
            if self.type is ElasticitySample:
                self.CSVConnector.insert(obj)
                return True
            row = [tuple(obj.__dict__.values())]
            self.DBConnector.insert(row)
        except Exception as e:
            print(e)
            return False
        return True

    def removeAll(self):
        try:
            self.DBConnector.remove()
        except Exception as e:
            print(e)
            return False
        return True

    def retrieveAll(self):

        return self.DBConnector.retrieve()

import json
from DBConnector import DBConnector


class StorageController:
    DBConnector = None
    type = None

    def __init__(self, dbConfig, type):
        self.type = type
        self.DBConnector = DBConnector(dbConfig)

    def save(self, obj):
        if type(obj) is not self.type:
            raise Exception('Invalid type')
        row = [tuple(obj.__dict__.values())]
        try:
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

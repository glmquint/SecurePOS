import json
from src.Storage.DBConnector import DBConnector
import pandas as pd


class StorageController:
    DBConnector = None
    type = None

    def __init__(self, dbConfig, type, messageBus):
        self.type = type
        self.DBConnector = DBConnector(dbConfig)
        self.messageBus = messageBus

    def save(self):
        obj = self.messageBus.popTopic("preparedSession")
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
        data_elem = self.DBConnector.retrieve()
        return [self.type(elem) for elem in data_elem]

    def countAll(self):
        return self.DBConnector.count()[0][0]

    def createTable(self):
        try:
            self.DBConnector.createTable()
        except Exception as e:
            # FIXME handle table already existing
            print(e)
            pass

    def normalizeData(self):
        pass
        preparedSessions = self.retrieveAll()
        tmp = []
        for p in preparedSessions:
            tmp.append(p.returnArray()[:len(p.returnArray()) - 1])

        dataframe_data = pd.DataFrame(tmp)
        print(dataframe_data)

        df_max_scaled = dataframe_data.copy()
        for column in df_max_scaled.columns:
            df_max_scaled[column] = df_max_scaled[column] / df_max_scaled[column].abs().max()

        # print dataframe data
        print(df_max_scaled)
        # TODO convert matrix to prepared session

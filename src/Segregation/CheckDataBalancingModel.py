from src.Segregation.PreparedSession import PreparedSession
from src.Storage.StorageController import *


class CheckDataBalancingModel:

    def __init__(self, storageController):
        self.__storageController = storageController
        return

    def retrivePreparedSession(self):
        dataReturned = self.__storageController.retrieveAll()
        preparedSession = []
        for i in dataReturned:
            preparedSession.append(PreparedSession(i))
        return preparedSession
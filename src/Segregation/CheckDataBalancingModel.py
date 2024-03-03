from src.Segregation.PreparedSession import PreparedSession
from src.Storage.StorageController import *


class CheckDataBalancingModel:

    def __init__(self, storageController):
        self.__storageController = storageController
        return

    def retrivePreparedSession(self):
        return self.__storageController.retrieveAll()

from src.Segregation.PreparedSession import PreparedSession

class CheckInputCoverageModel:
    def __init__(self, storageController):
        self.__storageController = storageController
        return

    def retrivePreparedSession(self):
        return self.__storageController.retrieveAll()

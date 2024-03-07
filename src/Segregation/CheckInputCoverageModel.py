from src.Segregation.PreparedSession import PreparedSession


class CheckInputCoverageModel:
    def __init__(self, storageController):
        self.__storageController = storageController
        self.__preparedSessionList = None

    def retrivePreparedSession(self):
        self.__preparedSessionList = self.__storageController.retrieveAll()

    def getPreparedSessionList(self):
        return self.__preparedSessionList

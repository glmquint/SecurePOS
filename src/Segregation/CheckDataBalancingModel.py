class CheckDataBalancingModel:

    def __init__(self, storageController):
        self.__storageController = storageController
        self.__preparedSessionList = None

    def retrivePreparedSession(self):
        self.__preparedSessionList = self.__storageController.retrieve_all(False)

    def getPreparedSessionList(self):
        return self.__preparedSessionList



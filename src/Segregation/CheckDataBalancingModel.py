from src.DataObjects.Session import PreparedSession
from src.Storage.StorageController import StorageController


class CheckDataBalancingModel:

    def __init__(self, storage_controller):
        self.__storage_controller: StorageController = storage_controller
        self.__prepared_session_list: [PreparedSession] = None

    def retrive_prepared_session(self, limit_prepared_session):
        self.__prepared_session_list = self.__storage_controller.retrieve_n(
            limit_prepared_session, True)

    def get_prepared_session_list(self) -> [PreparedSession]:
        return self.__prepared_session_list

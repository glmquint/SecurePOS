class CheckDataBalancingModel:

    def __init__(self, storageController):
        self.__storage_controller = storageController
        self.__prepared_session_list = None

    def retrive_prepared_session(self):
        self.__prepared_session_list = self.__storage_controller.retrieve_all(False)

    def get_prepared_session_list(self):
        return self.__prepared_session_list




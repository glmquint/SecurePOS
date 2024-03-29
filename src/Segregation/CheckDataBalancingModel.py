from src.DataObjects.Session import PreparedSession
from src.Storage.StorageController import StorageController


class CheckDataBalancingModel:
    """
    Model class responsible for handling data related to data balancing checks.

    Attributes:
    __storage_controller (StorageController): An instance of the storage controller
                                              used for data retrival.
    __prepared_session_list (list): A list to hold instances of PreparedSession objects.

    Methods:
    retrive_prepared_session(limit_prepared_session):
        Retrieves a specified number of prepared sessions from the storage controller.
    get_prepared_session_list() -> list:
        Returns the list of prepared sessions stored in __prepared_session_list.
    """

    def __init__(self, storage_controller):
        """
        Initializes the CheckDataBalancingModel with the given storage controller.

        Parameters:
        storage_controller (StorageController): The storage controller to use for data retrieval.
        """
        self.__storage_controller: StorageController = storage_controller
        self.__prepared_session_list: [PreparedSession] = None

    def retrieve_prepared_session(self, limit_prepared_session):
        """
        Retrieves a specified number of prepared sessions from the storage controller
        and stores them in __prepared_session_list.

        Parameters:
        limit_prepared_session (int): The number of prepared sessions to retrieve.
        """
        self.__prepared_session_list = self.__storage_controller.retrieve_n(
            limit_prepared_session, True)

    def get_prepared_session_list(self) -> [PreparedSession]:
        """
        Returns the list of prepared sessions stored in __prepared_session_list.

        Returns:
        list: A list of PreparedSession objects.
        """
        return self.__prepared_session_list

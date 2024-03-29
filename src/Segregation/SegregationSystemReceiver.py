import os
from threading import Thread
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.DataObjects.Session import PreparedSession
from src.Storage.StorageController import StorageController
from src.util import monitorPerformance


class PreparedSessionReceiver:
    """
    Class responsible for receiving and saving PreparedSession objects from JSON data.

    Attributes:
    __server (Server): An instance of the server to handle incoming requests.
    __storage_controller (StorageController): An instance of the storage controller
                                              used for saving the received PreparedSession objects.
    __port (int): The port number to run the server on.
    __endpoint (str): The endpoint path to receive the PreparedSession objects.
    """

    def __init__(self, storage_controller, port, endpoint):
        """
        Initializes the PreparedSessionReceiver with the given parameters.

        Parameters:
        storage_controller (StorageController): An instance of the storage controller
                                                used for saving the received PreparedSession
                                                objects.
        port (int): The port number to run the server on.
        endpoint (str): The endpoint path to receive the PreparedSession objects.
        """
        self.__server = Server()
        self.__storage_controller: StorageController = storage_controller
        self.__port = port
        self.__endpoint = endpoint

    def run(self):
        """
        Starts the server to listen for incoming requests.
        """
        self.__server.add_resource(
            JSONEndpoint,
            "/" + str(self.__endpoint),
            recv_callback=self.callback_prepared_session,
            json_schema_path=f"{os.path.dirname(__file__)}/../DataObjects/Schema/PreparedSessionSchema.json")

        thread = Thread(target=self.__server.run, kwargs={'port': self.__port})
        # This will allow the main thread to exit even if the server is still running
        thread.daemon = True
        thread.start()

    @monitorPerformance(should_sample_after=False)
    def callback_prepared_session(self, json_data):
        """
        Callback function to handle received JSON data and save the PreparedSession object.

        Parameters:
        json_data (dict): The JSON data representing the PreparedSession object.
        """
        self.__storage_controller.save(PreparedSession(**json_data))

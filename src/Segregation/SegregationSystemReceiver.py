from threading import Thread
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.DataObjects.PreparedSession import PreparedSession


class PreparedSessionReceiver:
    def __init__(self, messageBus,storage_controller):
        self.__server = Server()
        self.__storage_controller = storage_controller
        pass

    def run(self):
        self.__server.add_resource(JSONEndpoint, "/segregationSystem", recv_callback=self.callabackPreparedSession,
                                   json_schema_path="../DataObjects/Schema/PreparedSessionSchema.json")
        thread = Thread(target=self.__server.run)
        # this will allow the main thread to exit even if the server is still running
        thread.daemon = True
        thread.start()
        pass

    def callabackPreparedSession(self, json_data):
        self.__storage_controller.save(PreparedSession(json_data))
        pass

from threading import Thread
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.DataObjects.PreparedSession import PreparedSession


class PreparedSessionReceiver:
    def __init__(self, messageBus,port):
        self.__server = Server()
        self.__messageBus = messageBus
        self.__port = port
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
        #TODO inserire nel db direttamente da qui
        self.__messageBus.pushTopic("preparedSession", PreparedSession(json_data))
        pass

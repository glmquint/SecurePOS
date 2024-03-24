import os
from threading import Thread
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.DataObjects.Session import PreparedSession
from src.Storage.StorageController import StorageController
from src.util import monitorPerformance


class PreparedSessionReceiver:
    def __init__(self, storage_controller, port,endpoint):
        self.__server = Server()
        self.__storage_controller: StorageController = storage_controller
        self.__port = port
        self.__endpoint = endpoint
        pass

    # def run(self,port: int):
    def run(self):
        self.__server.add_resource(JSONEndpoint, "/"+str(self.__endpoint), recv_callback=self.callaback_prepared_session,
                                   json_schema_path=f"{os.path.dirname(__file__)}/../DataObjects/Schema/PreparedSessionSchema.json")
        # thread = Thread(target=self.__server.run,args=(port,))
        thread = Thread(target=self.__server.run,kwargs={'port': self.__port})
        # this will allow the main thread to exit even if the server is still running
        thread.daemon = True
        thread.start()
        pass

    @monitorPerformance(should_sample_after=False)
    def callaback_prepared_session(self, json_data):
        self.__storage_controller.save(PreparedSession(**json_data))
        pass


'''
class PreparedSessionReceiver:
    def __init__(self,storage_controller):
        self.__server = Server()
        self.__storage_controller : StorageController = storage_controller
        pass

    def run(self,port: int):

        self.__server.add_resource(JSONEndpoint, "/segregationSystem", recv_callback=self.callaback_prepared_session,
                                   json_schema_path=f"{os.path.dirname(__file__)}/../DataObjects/Schema/PreparedSessionSchema.json")
        thread = Thread(target=self.__server.run,args=(port,))
        # this will allow the main thread to exit even if the server is still running
        thread.daemon = True
        thread.start()
        pass

    def callaback_prepared_session(self, json_data):
        self.__storage_controller.save(PreparedSession(**json_data))
        pass


'''
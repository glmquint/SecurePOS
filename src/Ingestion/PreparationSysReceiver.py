from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController

DATAOBJ_PATH = "/src/DataObjects/Schema"

class PreparationSysReceiver:
    def __init__(self, storage_controller:StorageController, message_bus:MessageBus):
        self.storage_controller = storage_controller
        self.message_bus = message_bus
        self.server = Server()
        self.server.add_resource(JSONEndpoint, "/record", recv_callback=self.receiveRecord, json_schema_path=f"{DATAOBJ_PATH}/RecordSchema.json")
        self.server.add_resource(JSONEndpoint, "/raw_session", recv_callback=self.receiveRawSession, json_schema_path=f"{DATAOBJ_PATH}/RawSessionSchema.json")

    def receiveRecord(self, json_data):
        self.storage_controller.save(json_data)

    def receiveRawSession(self, json_data):
        self.message_bus.pushTopic("RawSession", json_data)

    def run(self):
        self.server.run()

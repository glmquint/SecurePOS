from threading import Thread

from src.DataObjects.Record import Record
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController
from src.util import log

DATAOBJ_PATH = "../DataObjects/Schema"


class PreparationSysReceiver:
    def __init__(self, storage_controller:StorageController, message_bus:MessageBus):
        self.storage_controller = storage_controller
        self.message_bus = message_bus
        self.server = Server()
        self.server.add_resource(JSONEndpoint, "/record", recv_callback=self.receiveRecord, json_schema_path=f"{DATAOBJ_PATH}/RecordSchema.json")
        self.server.add_resource(JSONEndpoint, "/raw_session", recv_callback=self.receiveRawSession, json_schema_path=f"{DATAOBJ_PATH}/RawSessionSchema.json")

    @log
    def receiveRecord(self, json_data):
        record = Record()
        record.__dict__ = json_data
        self.storage_controller.save(record)

    @log
    def receiveRawSession(self, json_data):
        self.message_bus.pushTopic("RawSession", json_data)

    def run(self):
        self.server.run()

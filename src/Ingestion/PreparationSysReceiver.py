from threading import Thread

from src.DataObjects.RecordOld import RecordOld
from src.DataObjects.Session import RawSession
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController
from src.util import log

DATAOBJ_PATH = "../DataObjects/Schema"


class PreparationSysReceiver:
    def __init__(self, raw_session_topic:str, storage_controller:StorageController, message_bus:MessageBus):
        self.raw_session_topic  = raw_session_topic
        self.storage_controller = storage_controller
        self.message_bus        = message_bus
        self.server             = Server()
        self.server.add_resource(JSONEndpoint, "/record", recv_callback=self.receiveRecord, json_schema_path=f"{DATAOBJ_PATH}/RecordSchema.json")
        self.server.add_resource(JSONEndpoint, "/raw_session", recv_callback=self.receiveRawSession, json_schema_path=f"{DATAOBJ_PATH}/RawSessionSchema.json")

    @log
    def receiveRecord(self, json_data):
        record = RecordOld(**json_data)
        self.storage_controller.save(record)

    @log
    def receiveRawSession(self, json_data):
        raw_session = RawSession(**json_data)
        self.message_bus.pushTopic(self.raw_session_topic, raw_session)

    def run(self):
        self.server.run()

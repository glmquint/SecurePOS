import os
from threading import Thread

from src.DataObjects.Record import LocalizationSysRecord, NetworkMonitorRecord, TransactionCloudRecord, Record, Label
from src.DataObjects.RecordOld import RecordOld
from src.DataObjects.Session import RawSession
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController
from src.util import log

DATAOBJ_PATH = f"{os.path.dirname(__file__)}/../DataObjects/Schema"


class PreparationSysReceiver:
    def __init__(self, config:dict, raw_session_topic:str, storage_controller:StorageController, message_bus:MessageBus):
        self.raw_session_topic  = raw_session_topic
        self.storage_controller = storage_controller
        self.message_bus        = message_bus
        self.server             = Server()
        for endpoint in config['endpoints']:
            self.server.add_resource(JSONEndpoint, endpoint['endpoint'], recv_callback=self.__getattribute__(endpoint['callback']), json_schema_path=f"{DATAOBJ_PATH}/{endpoint['schema']}")

    @log
    def receiveRecord(self, json_data):
        if not isinstance(json_data, dict):
            raise Exception(f"Expected dict, got {type(json_data)}")
        # change UUID filed into uuid
        expected_key = {
            'UUID': 'uuid',
            'LABEL': 'label',
            'latitude': 'location_latitude',
            'longitude': 'location_longitude',
            'targetIP': 'target_ip',
            'destIP': 'dest_ip',
            'timestamp': 'timestamp',
            'amount': 'amount'
        }
        if any(k not in expected_key.keys() for k in json_data.keys()):
            raise Exception(f"Expected {expected_key.keys()}, got {json_data.keys()}")
        json_data = {expected_key[k]: v for k, v in json_data.items()}
        if 'uuid' not in json_data:
            raise Exception(f"Expected uuid, got {json_data}")
        if 'location_latitude' in json_data or 'location_longitude' in json_data:
            record = LocalizationSysRecord(**json_data)
        elif 'target_ip' in json_data or 'dest_ip' in json_data:
            record = NetworkMonitorRecord(**json_data)
        elif 'timestamp' in json_data or 'amount' in json_data:
            record = TransactionCloudRecord(**json_data)
        elif "label" in json_data:
            record = Label(**json_data)
        else:
            raise Exception("unkown record type")
        if not self.storage_controller.save(record):
            raise Exception(f"Failed to save {record}")

    @log
    def receiveRawSession(self, json_data):
        parsed_json_data = {'records': [Record.from_row(**record) for record in json_data['records']]}
        raw_session = RawSession(**parsed_json_data)
        self.message_bus.pushTopic(self.raw_session_topic, raw_session)

    def run(self):
        self.server.run(port=5005) # TODO: make it configurable goddamit

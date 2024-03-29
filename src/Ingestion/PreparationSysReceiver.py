import os

from src.DataObjects.Record import LocalizationSysRecord, NetworkMonitorRecord, TransactionCloudRecord, Record, Label
from src.DataObjects.Session import RawSession
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController
from src.util import monitorPerformance

DATAOBJ_PATH = f"{os.path.dirname(__file__)}/../DataObjects/Schema"


class PreparationSysReceiver:
    """
    This class is responsible for receiving data from the preparation system and the client-side application.

    The PreparationSysReceiver class initializes various components such as the Server and JSONEndpoint for receiving
    records and raw sessions. These components are used to manage the receiving process,
    including validating the data against a JSON schema and saving it to the storage or pushing it to the message bus.

    Attributes:
        raw_session_topic (str): Topic for raw sessions in the message bus.
        storage_controller (StorageController): Manages storage-related operations.
        message_bus (MessageBus): Facilitates communication between different components.
        server (Server): Server for receiving data.
        port (int): Port number for the server.

    Methods:
        receiveRecord(json_data): Receives a record, validates it, and saves it to the storage.
        receiveRawSession(json_data): Receives a raw session, validates it, and pushes it to the message bus.
        run(): Starts the server for receiving data.
    """
    def __init__(
            self,
            config: dict,
            raw_session_topic: str,
            storage_controller: StorageController,
            message_bus: MessageBus):
        self.raw_session_topic = raw_session_topic
        self.storage_controller = storage_controller
        self.message_bus = message_bus
        self.server = Server()
        self.port = config['port']
        for endpoint in config['endpoints']:
            self.server.add_resource(
                JSONEndpoint,
                endpoint['endpoint'],
                recv_callback=self.__getattribute__(
                    endpoint['callback']),
                json_schema_path=f"{DATAOBJ_PATH}/{endpoint['schema']}")

    @monitorPerformance(should_sample_after=False)
    def receiveRecord(self, json_data):
        if not isinstance(json_data, dict):
            raise Exception(f"Expected dict, got {type(json_data)}")
        # Key Remapping Table (KRT)
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
            raise Exception(
                f"Expected {expected_key.keys()}, got {json_data.keys()}")
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
            raise Exception("unknown record type")
        if not self.storage_controller.save(record):
            raise Exception(f"Failed to save {record}")

    @monitorPerformance(should_sample_after=False)
    def receiveRawSession(self, json_data):
        parsed_json_data = {
            'records': [
                Record.from_row(
                    **record) for record in json_data['records']]}
        raw_session = RawSession(**parsed_json_data)
        self.message_bus.pushTopic(self.raw_session_topic, raw_session)

    def run(self):
        self.server.run(port=self.port)

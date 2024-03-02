from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server

DATAOBJ_PATH = "/src/DataObjects/Schema"

class PreparationSysReceiver:
    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.server = Server()
        self.server.add_resource(JSONEndpoint, "/record", recv_callback=self.receiveRecord, json_schema_path=f"{DATAOBJ_PATH}/AttackRiskLabelSchema.json")
        self.server.add_resource(JSONEndpoint, "/test_endpoint", recv_callback=self.receiveRawSession, json_schema_path=f"{DATAOBJ_PATH}/AttackRiskLabelSchema.json")

    def receiveRecord(self, json_data):
        pass

    def receiveRawSession(self, json_data):
        pass

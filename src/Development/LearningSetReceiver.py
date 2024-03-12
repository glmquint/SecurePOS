import json

from src.Development.LearningSet import LearningSet
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.JsonIO.JSONEndpoint import JSONEndpoint


class LearningSetReceiver:
    learning_set = None
    message_bus_ref = None
    server: Server = None

    def __init__(self, message_bus: MessageBus):
        self.message_bus_ref = message_bus
        self.server = Server()
        self.server.add_resource(JSONEndpoint, "/learning_set",
                                 recv_callback=self.receive_learning_set,
                                 json_schema_path="../../json_schema/learning_set_schema.json")

    def receive_learning_set(self,json_data):
        self.learning_set = LearningSet(json.loads(json_data))
        self.message_bus_ref.pushTopic("LearningSet", self.learning_set)
        return 200

    def run(self):
        self.server.run()

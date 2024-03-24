import json
import os

from src.DataObjects.LearningSet import LearningSet
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.util import monitorPerformance


class LearningSetReceiver:
    learning_set: LearningSet = None
    message_bus_ref: MessageBus = None
    server: Server = None

    def __init__(self, message_bus: MessageBus, endpoint_url: str):
        self.message_bus_ref = message_bus
        self.server = Server()
        self.server.add_resource(JSONEndpoint, endpoint_url,
                                 recv_callback=self.receive_learning_set,
                                 json_schema_path=f"{os.path.dirname(__file__)}/../DataObjects/Schema/learning_set_schema.json")

    @monitorPerformance(should_sample_after=False)
    def receive_learning_set(self, json_data):
        self.learning_set = LearningSet(json_data,True)
        self.message_bus_ref.pushTopic("LearningSet", self.learning_set)
        print(f'[{self.__class__.__name__}]: Learning set received and pushed to message bust')
        return 200

    def run(self, port: int):
        self.server.run(port=port)

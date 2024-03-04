from threading import Thread

from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus


class LabelReceiver:
    def __init__(self):
        self.server = Server()
        self.mbus = MessageBus(["label", "sec_label"])
        return

    def receive(self):
        # test_callback = lambda json_data: print(f"Hello from test_callback. Received {json_data}")
        self.server.add_resource(JSONEndpoint, "/test_endpoint", recv_callback=self.callback_f,
                                 json_schema_path="../DataObjects/Schema/AttackRiskLabelSchema.json")
        thread = Thread(target=self.server.run)
        thread.daemon = True
        thread.start()

    def callback_f(self, json_data):
        print(f"Received {json_data}")
        self.mbus.pushTopic("label", json_data)

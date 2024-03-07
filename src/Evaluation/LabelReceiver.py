from threading import Thread

from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus


class LabelReceiver:
    def __init__(self):
        self.server_label = Server()
        # self.server_sec = Server()
        self.mbus = MessageBus(["label", "sec_label"])
        return

    def receive(self):
        # test_callback = lambda json_data: print(f"Hello from test_callback. Received {json_data}")
        # self.server_sec.add_resource(JSONEndpoint, "/security_expert_endpoint", recv_callback=self.callback_s,
        #                             json_schema_path="../DataObjects/Schema/AttackRiskLabelSchema.json")
        self.server_label.add_resource(JSONEndpoint, "/label_endpoint", recv_callback=self.callback_f,
                                       json_schema_path="../DataObjects/Schema/AttackRiskLabelSchema.json")
        self.server_label.add_resource(JSONEndpoint, "/security_expert_endpoint", recv_callback=self.callback_s,
                                       json_schema_path="../DataObjects/Schema/AttackRiskLabelSchema.json")
        thread = Thread(target=self.server_label.run)
        # thread2 = Thread(target=self.server_sec.run)
        thread.daemon = True
        # thread2.daemon = True
        # thread2.start()
        thread.start()

    def callback_s(self, json_data):
        print(f"Received from security {json_data}")
        self.mbus.pushTopic("sec_label", json_data)

    def callback_f(self, json_data):
        print(f"Received {json_data}")
        self.mbus.pushTopic("label", json_data)

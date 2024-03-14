from threading import Thread

from src.DataObjects.AttackRiskLabel import AttackRiskLabel
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig


class LabelReceiver:
    def __init__(self):
        self.server = Server()
        self.mbus = MessageBus(["label", "sec_label"])
        self.scontroller_label = StorageController(DBConfig("evaluation", "labels", ("label",)),
            type(AttackRiskLabel(None)))
        self.scontroller_security = StorageController(DBConfig("evaluation", "security_labels", ("label",)),
            type(AttackRiskLabel(None)))
        return

    def receive(self):
        self.server.add_resource(JSONEndpoint, "/label_endpoint", recv_callback=self.callback_f,
                                 json_schema_path="../DataObjects/Schema/AttackRiskLabelSchema.json")
        self.server.add_resource(JSONEndpoint, "/security_expert_endpoint", recv_callback=self.callback_s,
                                 json_schema_path="../DataObjects/Schema/AttackRiskLabelSchema.json")
        thread = Thread(target=self.server.run)
        thread.daemon = True
        thread.start()

    def callback_s(self, json_data):
        #print(f"Received from security {json_data}")
        self.mbus.pushTopic("sec_label", json_data)
        self.scontroller_security.save(AttackRiskLabel(json_data["attackRiskLabel"]))

    def callback_f(self, json_data):
        #print(f"Received {json_data}")
        self.mbus.pushTopic("label", json_data)
        self.scontroller_label.save(AttackRiskLabel(json_data["attackRiskLabel"]))


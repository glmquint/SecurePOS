from threading import Thread


from src.DataObjects.AttackRiskLabel import AttackRiskLabel
from src.DataObjects.Record import Label
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig


class LabelReceiver:
    def __init__(self):
        self.server = Server()
        self.mbus = MessageBus(["label", "sec_label"])
        self.scontroller_label = StorageController({'name': 'evaluation', 'table_name': 'labels'},type(Label()))
        #self.scontroller_label = StorageController(DBConfig("evaluation", "labels"),
            #type(Label()))
        self.scontroller_security = StorageController({'name': 'evaluation', 'table_name': 'security_labels'},type(Label()))
        #self.scontroller_security = StorageController(DBConfig("evaluation", "security_labels"),
            #type(Label()))
        return

    def receive(self):
        self.server.add_resource(JSONEndpoint, "/label_endpoint", recv_callback=self.callback_f,
                                 json_schema_path="../DataObjects/Schema/Label.json")
        self.server.add_resource(JSONEndpoint, "/security_expert_endpoint", recv_callback=self.callback_s,
                                 json_schema_path="../DataObjects/Schema/Label.json")
        thread = Thread(target=self.server.run)
        thread.daemon = True
        thread.start()

    def callback_s(self, json_data):
        #print(f"Received from security {json_data}")
        #???
        data = Label(**json_data)
        #self.scontroller_security.save(Label(label=json_data["label"],uuid=json_data["uuid"]))
        self.scontroller_security.save(data)
        self.mbus.pushTopic("sec_label", data)

    def callback_f(self, json_data):
        #print(f"Received {json_data}")
        #???
        data = Label(**json_data)
        self.scontroller_label.save(data)
        self.mbus.pushTopic("label", data)


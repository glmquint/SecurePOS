# This class use the Server from JsonIO to add two resource one for session and one for classifier
from src.DataObjects.ClassifierTest import ClassifierTest
from src.DataObjects.PreparedSession import PreparedSession
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server


class ProductionSystemReceiver:
    def __init__(self, systemBus):
        self.systemBus = systemBus
        self.server = Server()
        self.server.add_resource(JSONEndpoint, "/PreparedSession",
                                 recv_callback=self.session_callback,
                                json_schema_path="../DataObjects/Schema/PreparedSessionSchema.json")
        self.server.add_resource(JSONEndpoint, "/Classifier",
                                 recv_callback=self.classifier_callback,
                                 json_schema_path="../DataObjects/Schema/ClassifierTestSchema.json")

    def session_callback(self, json_data):
        preparedSession = PreparedSession(**json_data)
        # push the preparedSession into the Messegebus
        self.systemBus.pushTopic("PreparedSession", preparedSession)
        print("Received PreparedSession")
        return 200

    def classifier_callback(self, json_data):
        classifierTest = ClassifierTest(**json_data)
        # print(classifierTest)
        # push the preparedSession into the Messegebus
        self.systemBus.pushTopic("Classifier", classifierTest)
        print("Received Classifier")
        return 200


    def run(self):
        self.server.run()


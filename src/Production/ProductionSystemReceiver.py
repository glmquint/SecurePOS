import joblib

from src.DataObjects.ClassifierTest import ClassifierTest
from src.DataObjects.PreparedSession import PreparedSession
from src.JsonIO.FileEndpoint import FileEndpoint
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server

class ProductionSystemReceiver:
    def __init__(self, systemBus):
        self.systemBus = systemBus
        self.server = Server()
        self.server.add_resource(JSONEndpoint, "/PreparedSession",
                                 recv_callback=self.session_callback,
                                json_schema_path="../DataObjects/Schema/PreparedSessionSchema.json")
        self.server.add_resource(FileEndpoint, "/Classifier",
                                 recv_callback=self.classifier_callback)

    def session_callback(self, json_data):
        preparedSession = PreparedSession(**json_data)
        # push the preparedSession into the Messegebus
        self.systemBus.pushTopic("PreparedSession", preparedSession)
        print("Received PreparedSession")
        return 200

    def classifier_callback(self, file):
        classifier = joblib.load(file)
        #classifierTest = ClassifierTest(classifier)
        # push the classifierTest into the Messegebus
        self.systemBus.pushTopic("Classifier", classifier)
        print("Received Classifier")
        return 200

    def run(self):
        self.server.run()


if __name__ == "__main__":
    pass
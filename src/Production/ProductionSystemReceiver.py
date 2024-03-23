import os.path

import joblib

from src.DataObjects.ClassifierTest import ClassifierTest
from src.DataObjects.Session import PreparedSession
from src.JsonIO.FileEndpoint import FileEndpoint
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server

class ProductionSystemReceiver:
    def __init__(self, port, systemBus):
        self.port = port
        self.systemBus = systemBus
        self.server = Server()
        self.server.add_resource(JSONEndpoint, "/PreparedSession",
                                 recv_callback=self.session_callback,
                                json_schema_path=f"{os.path.dirname(__file__)}/../DataObjects/Schema/PreparedSessionSchema.json")
        self.server.add_resource(FileEndpoint, "/Classifier",
                                 recv_callback=self.classifier_callback)

    def session_callback(self, json_data):
        #print(json_data)
        prepared_session = PreparedSession(**json_data)
        print("PreparedSession created")
        # push the preparedSession into the Messegebus
        self.systemBus.pushTopic("PreparedSession", prepared_session)
        print("Received PreparedSession")
        return 200

    def classifier_callback(self, file):
        classifier = joblib.load(file)
        # Save in a file called classifier.sav
        joblib.dump(classifier, f"{os.path.dirname(__file__)}/classifier.sav")
        print("Classifier received and saved")
        self.systemBus.pushTopic("Classifier", classifier)
        return 200


    def run(self):
        self.server.run(port=self.port)


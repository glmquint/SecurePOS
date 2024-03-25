import os.path
import joblib
from src.DataObjects.Session import PreparedSession
from src.JsonIO.FileEndpoint import FileEndpoint
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.util import monitorPerformance


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

    @monitorPerformance(should_sample_after=False)
    def session_callback(self, json_data):
        prepared_session = PreparedSession(**json_data)
        print("PreparedSession created")
        # push the prepared_session into the Messegebus
        self.systemBus.pushTopic("PreparedSession", prepared_session)
        print("Received PreparedSession")
        return 200

    @monitorPerformance(should_sample_after=False)
    def classifier_callback(self, file):
        classifier = joblib.load(file)
        # Save in a file called classifier.sav
        joblib.dump(classifier, f"{os.path.dirname(__file__)}/classifier.sav")
        print("Classifier received and saved")
        self.systemBus.pushTopic("Classifier", classifier)
        return 200

    def run(self):
        self.server.run(port=self.port)


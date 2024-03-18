# This class use the Server from JsonIO to add two resource one for session and one for classifier
import json
from src.DataObjects.ElasticitySample import ElasticitySample
from src.DataObjects.Message import Message
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.Storage.StorageController import StorageController


class MessagingReceiver:
#messaging system logs => to be logged
#timestamp message dei servizi => to be writed in the csv using csv connector
    def __init__(self, port=5001):
        self.server = Server()
        self.port = port
        self.server.add_resource(JSONEndpoint, "/MessagingSystem",
                                 recv_callback=self.message_callback,
                                json_schema_path="../DataObjects/Schema/MessageSchema.json")

        self.server.add_resource(JSONEndpoint, "/ElasticitySample",
                                 recv_callback=self.elasticity_callback,
                                 json_schema_path="../DataObjects/Schema/ElasticitySampleSchema.json")
    def message_callback(self, json_data):
        # Print the received message to a log file
        message = Message(**json_data)
        print(message)
        with open("MessageLog.txt", "a") as log:
            log.write(str(message) + "\n")
    def elasticity_callback(self, json_data):
        # Print the received message to a log file
        print(json_data)
        data_dict = json.loads(json_data)
        elasticity_sample = ElasticitySample(**data_dict)
        storage_controller = StorageController({"path": "elasticity.csv"}, ElasticitySample)
        storage_controller.save(elasticity_sample)

    def run(self):
        self.server.run(port=self.port)


if __name__ == "__main__":
    messagingReceiver = MessagingReceiver()
    messagingReceiver.run()
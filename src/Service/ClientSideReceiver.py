# This class use the Server from JsonIO to add two resource one for session and one for classifier
from src.DataObjects.Message import Message
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server


class ClientSideReceiver:
    def __init__(self, port=5000):
        self.server = Server()
        self.port = port
        self.server.add_resource(JSONEndpoint, "/ClientSideSystem",
                                 recv_callback=self.client_callback,
                                 json_schema_path="../DataObjects/Schema/MessageSchema.json")

    def client_callback(self, json_data):
        # Print the received message to a log file
        message = Message(**json_data)
        with open("ClientLog.txt", "a") as log:
            log.write(str(message) + "\n")


    def run(self):
        self.server.run(port=self.port)

from src.DataObjects.Message import Message
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server


class ServiceReceiver:
    def __init__(self):
        self.server = Server()
        self.server.add_resource(JSONEndpoint, "/MessagingSystem",
                                 recv_callback=self.message_callback,
                                json_schema_path="../DataObjects/Schema/MessageSchema.json")
        self.server.add_resource(JSONEndpoint, "/ClientSideSystem",
                                 recv_callback=self.client_callback,
                                 json_schema_path="../DataObjects/Schema/MessageSchema.json")

    def message_callback(self, json_data):
        # Print the received message to a log file
        message = Message(**json_data)
        with open("log.txt", "a") as log:
            log.write(str(message) + "\n")

    def client_callback(self, json_data):
        # Print the received message to a log file
        message = Message(**json_data)
        with open("log.txt", "a") as log:
            log.write(str(message) + "\n")


    def run(self):
        self.server.run()


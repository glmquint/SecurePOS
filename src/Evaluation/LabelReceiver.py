
import os
from threading import Thread


from src.DataObjects.Record import Label
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController
from src.util import monitorPerformance


class LabelReceiver:
    """
        This class is responsible for receiving labels from the messaging system. It initializes the server, message bus,
        storage controllers, and receives labels from the messaging system.

        Attributes:
            port: The port number.
            server: An object of Server that handles the server.
            mbus: An object of MessageBus that handles the message bus.
            scontroller_label: A StorageController object for labels.
            scontroller_security: A StorageController object for security labels.

        Methods:
            receive: Receives labels from the messaging system.
            callback_s: A callback function for security labels.
            callback_f: A callback function for labels.
    """
    def __init__(self, port=0):
        self.port = port
        self.server = Server()
        self.mbus = MessageBus(["label", "sec_label"])
        self.scontroller_label = StorageController(
            {'name': 'evaluation', 'table_name': 'labels'}, Label)
        self.scontroller_security = StorageController(
            {'name': 'evaluation', 'table_name': 'security_labels'}, Label)

    def receive(self):
        """receive function in another thread"""
        self.server.add_resource(
            JSONEndpoint,
            "/evaluation_label",
            recv_callback=self.callback_f,
            json_schema_path=f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json")
        self.server.add_resource(
            JSONEndpoint,
            "/evaluation_security_label",
            recv_callback=self.callback_s,
            json_schema_path=f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json")
        if self.port == 0:
            thread = Thread(target=self.server.run)
        else:
            thread = Thread(target=self.server.run, args=[False, self.port])
        thread.daemon = True
        thread.start()

    @monitorPerformance(should_sample_after=False)
    def callback_s(self, json_data):
        """"callback for the security labels"""
        data = Label(**json_data)
        print("Received security label.")
        print(data.uuid)
        print(data.label)
        self.scontroller_security.save(data)
        self.mbus.pushTopic("sec_label", data)

    @monitorPerformance(should_sample_after=False)
    def callback_f(self, json_data):
        """"callback for the labels"""
        print("Received label.")
        data = Label(**json_data)
        print(data.uuid)
        print(data.label)
        self.scontroller_label.save(data)
        self.mbus.pushTopic("label", data)

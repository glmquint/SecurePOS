import ipaddress
import os
import uuid
from threading import Thread
from time import sleep
from unittest import TestCase
import requests

from src.DataObjects.Classifier import Classifier
from src.DataObjects.Record import Label
from src.DataObjects.Session import PreparedSession
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Production.ProductionSystemOrchestrator import ProductionSystemOrchestrator
from src.Production.ProductionSystemReceiver import ProductionSystemReceiver


class IntegrationTest(TestCase):
    @classmethod
    def server_setup(self, port, systemBus):
        prodSysRec = ProductionSystemReceiver(port, systemBus)
        thread = Thread(target=prodSysRec.run)
        # this will allow the main thread to exit even if the server is still
        # running
        thread.daemon = True
        thread.start()

    @classmethod
    def main_setup(self):
        orchestrator = ProductionSystemOrchestrator()
        thread = Thread(target=orchestrator.run)
        # this will allow the main thread to exit even if the server is still
        # running
        thread.daemon = True
        thread.start()

    @classmethod
    def main_receiver(self):
        server = Server()

        def test_callback_evaluation(json_data): return print(
            f"Evaluation endpoint received {json_data}")
        def test_callback_client(json_data): return print(
            f"Client endpoint received {json_data}")
        server.add_resource(
            JSONEndpoint,
            "/evaluation",
            recv_callback=test_callback_evaluation,
            json_schema_path=f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json")
        server.add_resource(
            JSONEndpoint,
            "/client",
            recv_callback=test_callback_client,
            json_schema_path=f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json")
        threadServer = Thread(target=server.run, kwargs={'port': 5001})
        # this will allow the main thread to exit even if the server is still
        # running
        threadServer.daemon = True
        threadServer.start()

    def test_system_bus_send(self):
        systemBus = MessageBus(["PreparedSession", "Classifier"])
        self.server_setup(5003, systemBus)
        preparedSession = PreparedSession(
            mean_abs_diff_transaction=10,
            mean_abs_diff_transaction_amount=20,
            median_longitude=30,
            median_latitude=40,
            median_target_ip=int(
                ipaddress.ip_address("127.0.0.1")),
            median_dest_ip=int(
                ipaddress.ip_address("192.168.255.0")),
            label="high", uuid=str(uuid.uuid1()))

        classifierTest = Classifier()

        req = requests.post(
            "http://127.0.0.1:5003/PreparedSession",
            json=preparedSession.to_json())  # correct key
        assert req.status_code == 200
        print(systemBus.popTopic("PreparedSession"))
        with open('AverageClassifier.sav', 'rb') as f:
            req = requests.post(
                "http://127.0.0.1:5003/Classifier",
                files={
                    "uploaded": f})
            assert req.status_code == 200, f'Expected 200, got {req}'
        print(systemBus.popTopic("Classifier"))

    def test_production_switch(self):
        self.main_setup()
        self.main_receiver()
        preparedSession = PreparedSession(
            mean_abs_diff_transaction=10,
            mean_abs_diff_transaction_amount=20,
            median_longitude=30,
            median_latitude=40,
            median_target_ip=int(
                ipaddress.ip_address("127.0.0.1")),
            median_dest_ip=int(
                ipaddress.ip_address("192.168.255.0")),
            label="high", uuid=str(uuid.uuid1()))

        with open('AverageClassifier.sav', 'rb') as f:
            req = requests.post(
                "http://127.0.0.1:5003/Classifier",
                files={
                    "uploaded": f})
            assert req.status_code == 200, f'Expected 200, got {req}'


        for i in range(0, 10):
            req = requests.post(
                "http://127.0.0.1:5003/PreparedSession",
                json=preparedSession.to_json())  # correct key
            assert req.status_code == 200

        input("Press Enter to continue...")

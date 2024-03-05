from threading import Thread
from time import sleep
from unittest import TestCase

import requests

from src.DataObjects.AttackRiskLabel import AttackRiskLabel
from src.DataObjects.ClassifierTest import ClassifierTest
from src.DataObjects.PreparedSession import PreparedSession
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Production.ProductionSystemOrchestrator import ProductionSystemOrchestrator
from src.Production.ProductionSystemReceiver import ProductionSystemReceiver


class IntegrationTest(TestCase):
    @classmethod
    def server_setup(self, systemBus):
        prodSysRec = ProductionSystemReceiver(systemBus)
        thread = Thread(target=prodSysRec.run)
        thread.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread.start()

    @classmethod
    def main_setup(self):
        orchestrator = ProductionSystemOrchestrator()
        thread = Thread(target=orchestrator.run)
        thread.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread.start()

    @classmethod
    def main_receiver(self):
        server = Server()
        test_callback_evaluation = lambda json_data: print(f"Evaluation endpoint received {json_data}")
        test_callback_client = lambda json_data: print(f"Client endpoint received {json_data}")
        server.add_resource(JSONEndpoint, "/evaluation", recv_callback=test_callback_evaluation,
                            json_schema_path="../DataObjects/Schema/AttackRiskLabelSchema.json")
        server.add_resource(JSONEndpoint, "/client", recv_callback=test_callback_client,
                            json_schema_path="../DataObjects/Schema/AttackRiskLabelSchema.json")
        threadServer = Thread(target=server.run, kwargs={'port':5001})
        threadServer.daemon = True  # this will allow the main thread to exit even if the server is still running
        threadServer.start()

    def test_system_bus_send(self):
        systemBus = MessageBus(["PreparedSession", "Classifier"])
        self.server_setup(systemBus)
        preparedSession = PreparedSession(10.5, 25.5,
                                          (-73.9857, 40.7484), "192.168.1.1",
                                          "203.0.113.5")
        classifierTest = ClassifierTest("test")

        req = requests.post("http://127.0.0.1:5000/PreparedSession", json=preparedSession.to_json())  # correct key
        assert req.status_code == 200
        print(systemBus.popTopic("PreparedSession"))
        req = requests.post("http://127.0.0.1:5000/Classifier", json=classifierTest.to_json())  # correct key
        assert req.status_code == 200
        print(systemBus.popTopic("Classifier"))

    def test_main(self):
        self.main_setup()
        self.main_receiver()
        preparedSession = PreparedSession(10.5, 25.5,
                                          (-73.9857, 40.7484), "192.168.1.1",
                                          "203.0.113.5")
        preparedSession1 = PreparedSession("alpha", 95.5,
                                          (-73.9857, 40.7484), "192.168.1.1",
                                          "192.168.1.1")
        attackRiskLabel = AttackRiskLabel("medium")
        reparedSession3 = PreparedSession()
        classifierTest = ClassifierTest("test")
        req = requests.post("http://127.0.0.1:5000/PreparedSession", json=preparedSession.to_json())
        assert req.status_code == 200   # correct key
        req = requests.post("http://127.0.0.1:5000/Classifier", json=classifierTest.to_json())
        assert req.status_code == 200   # correct key
        sleep(0.1)
        req = requests.post("http://127.0.0.1:5000/PreparedSession", json=preparedSession1.to_json())
        assert req.status_code == 400   # wrong type
        sleep(0.1)
        req = requests.post("http://127.0.0.1:5000/PreparedSession", json=attackRiskLabel.to_json())
        assert req.status_code == 400   # wrong data
        sleep(0.1)
        req = requests.post("http://127.0.0.1:5000/PreparedSession", json=classifierTest.to_json())
        assert req.status_code == 400   # wrong endpoint
        sleep(0.1)
        req = requests.post("http://127.0.0.1:5000/PreparedSession", json=reparedSession3.to_json())
        assert req.status_code == 400   # wrong format
        sleep(5)

    def test_production_switch(self):
        self.main_setup()
        self.main_receiver()
        preparedSession = PreparedSession(10.5, 25.5,
                                          (-73.9857, 40.7484), "192.168.1.1",
                                          "203.0.113.5")
        classifierTest = ClassifierTest("test")
        req = requests.post("http://127.0.0.1:5000/Classifier", json=classifierTest.to_json())  # correct key
        assert req.status_code == 200
        for i in range(0, 5):
            req = requests.post("http://127.0.0.1:5000/PreparedSession", json=preparedSession.to_json())  # correct key
            assert req.status_code == 200

        sleep(10)


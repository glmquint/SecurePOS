import ipaddress
from socket import inet_aton

from threading import Thread
from time import sleep
from unittest import TestCase

import joblib
import requests
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


from src.DataObjects.ClassifierTest import ClassifierTest
from src.DataObjects.Record import Label
from src.DataObjects.Session import PreparedSession
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
                            json_schema_path="../DataObjects/Schema/Label.json")
        server.add_resource(JSONEndpoint, "/client", recv_callback=test_callback_client,
                            json_schema_path="../DataObjects/Schema/Label.json")
        threadServer = Thread(target=server.run, kwargs={'port':5001})
        threadServer.daemon = True  # this will allow the main thread to exit even if the server is still running
        threadServer.start()

    def test_system_bus_send(self):
        systemBus = MessageBus(["PreparedSession", "Classifier"])
        self.server_setup(systemBus)
        preparedSession = PreparedSession(mean_abs_diff_transaction=10, mean_abs_diff_transaction_amount=20,
                                          median_longitude=30, median_latitude=40,
                                          median_target_ip= int(ipaddress.ip_address("127.0.0.1")),
                                          median_dest_ip= int(ipaddress.ip_address("192.168.255.0")),
                                          attack_risk_label=None)

        classifierTest = ClassifierTest("test")

        req = requests.post("http://127.0.0.1:5002/PreparedSession", json=preparedSession.to_json())  # correct key
        assert req.status_code == 200
        print(systemBus.popTopic("PreparedSession"))
        with open('AverageClassifier.sav', 'rb') as f:
            req = requests.post("http://127.0.0.1:5002/Classifier", files={"uploaded": f})
            assert req.status_code == 200, f'Expected 200, got {req}'
        print(systemBus.popTopic("Classifier"))

    def test_main(self):
        self.main_setup()
        self.main_receiver()
        preparedSession = PreparedSession(mean_abs_diff_transaction=10, mean_abs_diff_transaction_amount=20,
                                          median_longitude=30, median_latitude=40,
                                          median_target_ip=int(ipaddress.ip_address("127.0.0.1")),
                                          median_dest_ip=int(ipaddress.ip_address("192.168.255.0")),
                                          attack_risk_label=None)

        preparedSession1 = PreparedSession(mean_abs_diff_transaction="10", mean_abs_diff_transaction_amount=20,
                                          median_longitude="30", median_latitude=40,
                                          median_target_ip=int(ipaddress.ip_address("127.0.0.1")),
                                          median_dest_ip=int(ipaddress.ip_address("192.168.255.0")),
                                          attack_risk_label=None)

        attackRiskLabel = Label(label="medium", uuid="12345")
        preparedSession2 = PreparedSession(mean_abs_diff_transaction=None, mean_abs_diff_transaction_amount=None,
                                          median_longitude=None, median_latitude=None,
                                          median_target_ip=0,
                                          median_dest_ip=0,
                                          attack_risk_label=None)
        classifierTest = ClassifierTest("test")
        req = requests.post("http://127.0.0.1:5002/PreparedSession", json=preparedSession.to_json())
        assert req.status_code == 200   # correct key
        with open('AverageClassifier.sav', 'rb') as f:
            req = requests.post("http://127.0.0.1:5002/Classifier", files={"uploaded": f})
            assert req.status_code == 200, f'Expected 200, got {req}'
        sleep(0.1)
        req = requests.post("http://127.0.0.1:5002/PreparedSession", json=preparedSession1.to_json())
        assert req.status_code == 400   # wrong type
        sleep(0.1)
        req = requests.post("http://127.0.0.1:5002/PreparedSession", json=attackRiskLabel.to_json())
        assert req.status_code == 400   # wrong data
        sleep(0.1)
        req = requests.post("http://127.0.0.1:5002/PreparedSession", json=classifierTest.to_json())
        assert req.status_code == 400   # wrong endpoint
        sleep(0.1)
        req = requests.post("http://127.0.0.1:5002/PreparedSession", json=preparedSession2.to_json())
        assert req.status_code == 400   # wrong format
        sleep(5)

    def test_production_switch(self):
        self.main_setup()
        self.main_receiver()
        preparedSession = PreparedSession(mean_abs_diff_transaction=10, mean_abs_diff_transaction_amount=20,
                                          median_longitude=30, median_latitude=40,
                                          median_target_ip=int(ipaddress.ip_address("127.0.0.1")),
                                          median_dest_ip=int(ipaddress.ip_address("192.168.255.0")),
                                          attack_risk_label=None)
        with open('AverageClassifier.sav', 'rb') as f:
            req = requests.post("http://127.0.0.1:5003/Classifier", files={"uploaded": f})
            assert req.status_code == 200, f'Expected 200, got {req}'
        for i in range(0, 5):
            req = requests.post("http://127.0.0.1:5003/PreparedSession", json=preparedSession.to_json())  # correct key
            assert req.status_code == 200

        sleep(10)

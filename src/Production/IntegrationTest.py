from socket import inet_aton

from threading import Thread
from time import sleep
from unittest import TestCase

import joblib
import requests
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

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
        preparedSession = PreparedSession(["12345", 10, 20, 30, 40, "192.168.0.1", "192.168.0.2", "medium"])
        classifierTest = ClassifierTest("test")

        req = requests.post("http://127.0.0.1:5000/PreparedSession", json=preparedSession.to_json())  # correct key
        assert req.status_code == 200
        print(systemBus.popTopic("PreparedSession"))
        with open('AverageClassifier.sav', 'rb') as f:
            req = requests.post("http://127.0.0.1:5000/Classifier", files={"uploaded": f})
            assert req.status_code == 200, f'Expected 200, got {req}'
        print(systemBus.popTopic("Classifier"))

    def test_main(self):
        self.main_setup()
        self.main_receiver()
        preparedSession = PreparedSession(["12345", 10, 20, 30, 40, "192.168.0.1", "192.168.0.2", "medium"])
        preparedSession1 = PreparedSession(["12345", "10", 20, 30, 40, 192.16, "192.168.0.2", "medium"])
        attackRiskLabel = AttackRiskLabel("medium")
        reparedSession3 = PreparedSession([None, None, None, None, None, None, None, None])
        classifierTest = ClassifierTest("test")
        req = requests.post("http://127.0.0.1:5000/PreparedSession", json=preparedSession.to_json())
        assert req.status_code == 200   # correct key
        with open('AverageClassifier.sav', 'rb') as f:
            req = requests.post("http://127.0.0.1:5000/Classifier", files={"uploaded": f})
            assert req.status_code == 200, f'Expected 200, got {req}'
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
        preparedSession = PreparedSession(["12345", 10, 20, 30, 40, "192.168.0.1", "192.168.0.2", "medium"])
        with open('AverageClassifier.sav', 'rb') as f:
            req = requests.post("http://127.0.0.1:5000/Classifier", files={"uploaded": f})
            assert req.status_code == 200, f'Expected 200, got {req}'
        for i in range(0, 5):
            req = requests.post("http://127.0.0.1:5000/PreparedSession", json=preparedSession.to_json())  # correct key
            assert req.status_code == 200

        sleep(10)

    def test_real_classfier(self):
        self.main_setup()
        self.main_receiver()
        preparedSession = PreparedSession(["12345", 10, 20, 30, 40, "192.168.0.1", "192.168.0.2", "medium"])
        with open('AverageClassifier.sav', 'rb') as f:
            req = requests.post("http://127.0.0.1:5000/Classifier", files={"uploaded": f})
            assert req.status_code == 200, f'Expected 200, got {req}'
        req = requests.post("http://127.0.0.1:5000/PreparedSession", json=preparedSession.to_json())
        assert req.status_code == 200  # correct key
        sleep(5)

    def test_internal(self):
        from sklearn.neural_network import MLPClassifier
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import Pipeline
        import joblib

        # Load the trained classifier
        mlp_classifier = joblib.load('AverageClassifier.sav')

        # Define a function to predict the Attack Risk Label
        def predict_attack_risk(prepared_session):
            # Transform the input features as necessary
            import ipaddress
            prepared_session_features = [
                prepared_session.getMeanAbsoluteDifferencingTransactionAmount(),
                prepared_session.getMeanAbsoluteDifferencingTransactionTimestamps(),
                prepared_session.getMedianLatitude(),
                prepared_session.getMedianLongitude(),
                int(ipaddress.ip_address(prepared_session.getMedianTargetIP())),
                int(ipaddress.ip_address(prepared_session.getMedianDestIP()))
            ]
            # Predict the Attack Risk Label
            attack_risk_label = mlp_classifier.predict([prepared_session_features])[0]

            return attack_risk_label

        # Example usage:
        # Create a Prepared Session object
        prepared_session = PreparedSession(["12345", 10, 20, 30, 40, "192.168.0.1", "192.168.0.2", "medium"])

        # Predict the Attack Risk Label
        predicted_label = predict_attack_risk(prepared_session)
        print("Predicted Attack Risk Label:", predicted_label)

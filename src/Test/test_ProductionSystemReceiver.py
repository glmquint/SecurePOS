from threading import Thread
from time import sleep
from unittest import TestCase

import joblib
import requests
from sklearn.neural_network import MLPClassifier

from src.MessageBus.MessageBus import MessageBus
from src.Production.ProductionSystemReceiver import ProductionSystemReceiver


class TestProductionSystemReceiver(TestCase):
    def server_setup(self, systemBus):
        prodSysRec = ProductionSystemReceiver(systemBus)
        thread = Thread(target=prodSysRec.run)
        # this will allow the main thread to exit even if the server is still
        # running
        thread.daemon = True
        thread.start()

    def test_classifier_callback(self):
        systemBus = MessageBus(["PreparedSession", "Classifier"])
        self.server_setup(systemBus)
        # Create and train a simple MLP classifier
        clf = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500)
        # Assuming you have your training data X_train, y_train
        # clf.fit(X_train, y_train)

        # Save the classifier to a file
        joblib.dump(clf, 'classifier.pkl')
        with open('classifier.pkl', 'rb') as f:
            req = requests.post(
                "http://127.0.0.1:5000/Classifier",
                files={
                    "uploaded": f})
            assert req.status_code == 200, f'Expected 200, got {req}'

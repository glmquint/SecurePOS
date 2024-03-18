from datetime import datetime
from threading import Thread
from time import sleep
from unittest import TestCase
import requests

from src.DataObjects.ElasticitySample import ElasticitySample
from src.Service.MessagingReceiver import MessagingReceiver


class TestMessagingReceiver(TestCase):

    @classmethod
    def MessagingReceiverSetup(self):
        messagingReceiver = MessagingReceiver()
        thread_client_side = Thread(target=messagingReceiver.run())
        thread_client_side.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread_client_side.start()

    def test_message_callback(self):
        self.MessagingReceiverSetup()
        res = requests.post("http://127.0.0.1:5000/MessagingSystem", json={"message": "Hello"})
        assert res.status_code == 200


    def test_elasticity_callback(self):
        self.MessagingReceiverSetup()
        for i in range(0, 11):
            elasticity_sample = ElasticitySample("Test", "Start", datetime.now())
            res = requests.post("http://127.0.0.1:5000/ElasticitySample", json=elasticity_sample.to_json())
            assert res.status_code == 200
            sleep(1)
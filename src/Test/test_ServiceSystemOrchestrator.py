from datetime import datetime
from threading import Thread
from time import sleep
from unittest import TestCase

import requests

from src.DataObjects.ElasticitySample import ElasticitySample
from src.JsonIO.JSONSender import JSONSender
from src.Service.ServiceSystemOrchestrator import ServiceSystemOrchestator


class TestServiceSystemOrchestator(TestCase):
    @classmethod
    def main_setup(self):
        main = ServiceSystemOrchestator()
        thread = Thread(target=main.start)
        thread.daemon = True
        thread.start()

    def test_on_wait(self):
        self.main_setup()
        sender = JSONSender("../DataObjects/Schema/MessageSchema.json",
                            "http://127.0.0.1:5000/ClientSideSystem")
        ret = sender.send({"message": "Hello"})
        assert ret == True
        import os
        os.remove("../Service/ClientLog.txt")


    def test_message_callback(self):
        self.main_setup()
        res = requests.post("http://127.0.0.1:5001/MessagingSystem", json={"message": "Hello"})
        assert res.status_code == 200


    def test_elasticity_callback(self):
        self.main_setup()
        for i in range(0, 2):
            elasticity_sample = ElasticitySample("Test", "Start", datetime.now())
            res = requests.post("http://127.0.0.1:5001/ElasticitySample", json=elasticity_sample.to_json())
            assert res.status_code == 200
            sleep(1)

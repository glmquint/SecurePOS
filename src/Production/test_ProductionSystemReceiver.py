import json
from threading import Thread
from unittest import TestCase

import requests

from src.MessageBus.MessageBus import MessageBus
from src.Production.ProductionSystemReceiver import ProductionSystemReceiver
from src.DataObjects.PreparedSession import PreparedSession

class TestProductionSystemReceiver(TestCase):
    @classmethod
    def server_setup(self, systemBus):
        prodSysRec = ProductionSystemReceiver(systemBus)
        thread = Thread(target=prodSysRec.run)
        thread.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread.start()

    def test_send(self):
        systemBus = MessageBus(["PreparedSession", "Classifier"])
        self.server_setup(systemBus)
        preparedSession = PreparedSession(10.5, 25.5,
                           (-73.9857, 40.7484), "192.168.1.1",
                               "203.0.113.5")

        req = requests.post("http://127.0.0.1:5000/PreparedSession", json=preparedSession.to_json())  # correct key
        assert req.status_code == 200
        print(systemBus.popTopic("PreparedSession"))
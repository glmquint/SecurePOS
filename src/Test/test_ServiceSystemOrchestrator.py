from unittest import TestCase

from src.JsonIO.JSONSender import JSONSender


class TestServiceSystemOrchestator(TestCase):
    def test_on_wait(self):
        sender = JSONSender("../DataObjects/Schema/MessageSchema.json",
                            "http://127.0.0.1:5000/ClientSideSystem")
        ret = sender.send({"message": "Hello"})
        assert ret == True
        import os
        os.remove("../Service/ClientLog.txt")




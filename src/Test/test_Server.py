import os
import signal
import unittest
from multiprocessing import Process
from threading import Thread
from flask import request

import requests
from src.JsonIO.Server import Server
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.Test.test_JSONSender import server_setup


class TestServer(unittest.TestCase):
    @classmethod
    def server_setup(self):
        server = Server()
        def test_callback(json_data): return print(
            f"Hello from test_callback. Received {json_data}")
        server.add_resource(
            JSONEndpoint,
            "/test_endpoint",
            recv_callback=test_callback,
            json_schema_path=f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json")

        Thread(target=server.run, daemon=True).start()

    def test_add_resource(self):  # 100% coverage
        server_setup()

        req = requests.post(
            "http://127.0.0.1:5000/test_endpoint",
            json={
                "attackRiskLabel": "low"})  # correct key
        assert req.status_code == 200

        req = requests.post(
            "http://127.0.0.1:5000/test_endpoint",
            json={
                "attackRiskLabe": "low"})  # misspelled key
        assert req.status_code == 400

        req = requests.post(
            "http://127.0.0.1:5000/test_endpoint",
            data="not valid json")  # not json
        assert req.status_code == 460

        req = requests.post(
            "http://127.0.0.1:5000/invalid_endpoint",
            json={
                "attackRiskLabel": "low"})  # invalid endpoint
        assert req.status_code == 404

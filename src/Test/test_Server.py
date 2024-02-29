import os
import signal
from multiprocessing import Process
from threading import Thread
from flask import request

import requests
from src.JsonIO.Server import Server
from src.JsonIO.JSONEndpoint import JSONEndpoint

def server_setup():
    server = Server()
    test_callback = lambda json_data: print(f"Hello from test_callback. Received {json_data}")
    server.add_resource(JSONEndpoint, "/test_endpoint", recv_callback=test_callback, json_schema_path="../DataObjects/Schema/AttackRiskLabelSchema.json")

    # start server without blocking the main thread
    thread = Thread(target=server.run)
    thread.daemon = True
    thread.start()

def test_add_resource():
    server_setup()

    req = requests.post("http://127.0.0.1:5000/test_endpoint", json={"attackRiskLabel": "low"})
    assert req.status_code == 200


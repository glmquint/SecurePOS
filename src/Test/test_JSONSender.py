import os
from threading import Thread
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server


def server_setup():
    server = Server()
    def test_callback(json_data): return print(
        f"Hello from test_callback. Received {json_data}")
    server.add_resource(
        JSONEndpoint,
        "/test_endpoint",
        recv_callback=test_callback,
        json_schema_path=f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json")
    thread = Thread(target=server.run)
    # this will allow the main thread to exit even if the server is still
    # running
    thread.daemon = True
    thread.start()


def test_send():
    server_setup()
    sender = JSONSender(
        f"{os.path.dirname(__file__)}/../DataObjects/Schema/Label.json",
        "http://127.0.0.1:5000/test_endpoint")
    assert sender.send({"attackRiskLabel": "low"})
    assert sender.send({"invalid": "low"}) == False

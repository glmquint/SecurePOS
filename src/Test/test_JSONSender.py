from threading import Thread
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server

def server_setup():
    server = Server()
    test_callback = lambda json_data: print(f"Hello from test_callback. Received {json_data}")
    server.add_resource(JSONEndpoint, "/test_endpoint", recv_callback=test_callback, json_schema_path="../DataObjects/Schema/AttackRiskLabelSchema.json")
    thread = Thread(target=server.run)
    thread.daemon = True # this will allow the main thread to exit even if the server is still running
    thread.start()

def test_send():
    server_setup()
    sender = JSONSender("../DataObjects/Schema/AttackRiskLabelSchema.json", "http://127.0.0.1:5000/test_endpoint")
    assert sender.send({"attackRiskLabel": "low"}) == True
    assert sender.send({"invalid": "low"}) == False

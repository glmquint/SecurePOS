import requests
from src.JsonIO.Server import Server
from src.JsonIO.JSONEndpoint import JSONEndpoint

def setup_server():
    server = Server()
    def test_callback(json_data):
        print(json_data)
        pass
    test_endpoint = JSONEndpoint(test_callback, "../DataObjects/Schema/AttackRiskLabelSchema.json")
    server.add_resource(resource=test_endpoint, url="/test_endpoint")
    server.run(debug=False)

def test_add_resource():
    # setup on a new thread
    import threading
    server_thread = threading.Thread(target=setup_server)
    server_thread.start()
    # test
    r = requests.post("http://localhost:5000/test_endpoint", json={"test": "test"})
    print(r)
    input()
    assert r.status_code == 200

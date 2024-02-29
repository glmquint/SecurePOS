from flask import Flask, request
from flask_restful import Resource, Api

from src.JsonIO.JSONEndpoint import JSONEndpoint


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

    def run(self, debug=False):
        self.app.run(debug=debug)

    def add_resource(self, resource, url, **kwargs):
        self.api.add_resource(resource, url, endpoint=url, kwargs=kwargs)


if __name__ == "__main__":
    server = Server()
    def test_callback(json_data):
        print(json_data)
        pass
    server.add_resource(JSONEndpoint, "/test_endpoint", recv_callback=test_callback, json_schema_path="../DataObjects/Schema/AttackRiskLabelSchema.json")
    server.run(debug=True)
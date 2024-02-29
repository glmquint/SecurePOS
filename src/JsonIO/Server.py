from flask import Flask, request
from flask_restful import Resource, Api

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

    def run(self, debug=False):
        self.app.run(debug=debug)

    def add_resource(self, resource, url):
        self.api.add_resource(resource, url)

if __name__ == "__main__":
    server = Server()
    server.run(debug=True)
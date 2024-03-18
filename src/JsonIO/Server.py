import os
import signal
import sys

from flask import Flask, request
from flask_restful import Resource, Api

from src.JsonIO.JSONEndpoint import JSONEndpoint


class Server:
    def __init__(self, timeout=None):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.timeout = timeout

    def run(self, debug=False, port=5002):
        self.app.run(debug=debug, use_reloader=False, port=port) # don't use reloader in threaded environment

    def add_resource(self, resource, url, **kwargs):
        self.api.add_resource(resource, url, endpoint=url, resource_class_kwargs=kwargs)


if __name__ == "__main__":
   pass
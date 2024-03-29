from flask import Flask, request
from flask_restful import Resource, Api

class Server:
    """
        This class is responsible for creating a Flask server that listens for POST requests.

        Attributes:
            app: A Flask object that represents the server.
            api: A Flask-RESTful Api object that is used to add resources to the server.
            timeout: An integer representing the timeout for the server.

        Methods:
            run: Starts the server.
            add_resource: Adds a resource to the server.
    """
    def __init__(self, timeout=None):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.timeout = timeout

    def run(self, debug=False, port=5002):
        # don't use reloader in threaded environment
        self.app.run(
            debug=debug,
            use_reloader=False,
            port=port,
            host='0.0.0.0')

    def add_resource(self, resource, url, **kwargs):
        self.api.add_resource(
            resource,
            url,
            endpoint=url,
            resource_class_kwargs=kwargs)


if __name__ == "__main__":
    s = Server()
    s.run()

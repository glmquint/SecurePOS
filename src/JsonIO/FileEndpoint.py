from flask import request
from flask_restful import Resource, Api

class FileEndpoint(Resource):
    """
        This class is a Flask-RESTful Resource that handles POST requests to a specific endpoint.
        It is initialized with a callback function that is called when a file is received.

        Attributes:
            recv_callback: A callback function that is called when a file is received.

        Methods:
            post: Handles POST requests. It retrieves the file from the request,
            checks if a file was provided, calls the callback function with the file as an argument,
            and returns a response.
    """
    def __init__(self, **kwargs):
        self.recv_callback = kwargs['recv_callback']

    def post(self, **kwargs):
        file = request.files['uploaded']
        if file.filename == '':
            return "Expected file", 460
        self.recv_callback(file)
        return "OK", 200

from flask import request
from flask_restful import Resource, Api
from src.JsonIO.JsonValidator import JSONValidator


class JSONEndpoint(Resource):
    """
        This class is a Flask-RESTful Resource that handles POST requests to a specific endpoint.
        It is initialized with a callback function that is called when a request is received.

        Attributes:
            recv_callback: A callback function that is called when a JSON object is received.
            request_callback: A callback function that is called when a request is received.
            json_validator: A JSONValidator object that is used to validate the JSON object.

        Methods:
            post: Handles POST requests. It retrieves the JSON object from the request,
            checks if a JSON object was provided, validates the JSON object, calls the recv_callback function
            with the JSON object as an argument, calls the request_callback function with the request as an argument,
            and returns a response.
    """
    def __init__(self, **kwargs):
        self.recv_callback = kwargs.get('recv_callback', None)
        self.request_callback = kwargs.get('request_callback', None)
        self.json_validator = JSONValidator(kwargs['json_schema_path'])

    def post(self, **kwargs):
        if not request.is_json:
            return "Expected JSON", 460
        json_data = request.get_json()
        try:
            self.json_validator.validate_data(json_data)
            if self.recv_callback:
                self.recv_callback(json_data)
            if self.request_callback:
                self.request_callback(request)
            return "OK", 200
        except Exception as e:
            print(e, __name__)
            return "Bad Request", 400

from flask import request
from flask_restful import Resource, Api
import JSONValidator

class JSONEndpoint(Resource):
    def __init__(self, recv_callback : callable, json_schema_path : str):
        self.recv_callback = recv_callback
        self.json_schema_path = json_schema_path
        self.json_validator = JSONValidator(self.json_schema_path)

    def post(self):
        json_data = request.get_json()
        if self.json_validator.validate(json_data):
            self.recv_callback(json_data)
            return "OK", 200
        else:
            return "Bad Request", 400


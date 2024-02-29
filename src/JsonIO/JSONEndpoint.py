from flask import request
from flask_restful import Resource, Api
from src.JsonIO.JsonValidator import JSONValidator

class JSONEndpoint(Resource):

    def __init__(self, **kwargs):
        self.recv_callback = kwargs['recv_callback']
        self.json_validator = JSONValidator(kwargs['json_schema_path'])

    def post(self, **kwargs):
        if not request.is_json:
            return "Expected JSON", 460
        json_data = request.get_json()
        try:
            self.json_validator.validate_data(json_data)
            self.recv_callback(json_data)
            return "OK", 200
        except Exception as e:
            print(e)
            return "Bad Request", 400


from flask import request
from flask_restful import Resource, Api
from src.JsonIO.JsonValidator import JSONValidator

class JSONEndpoint(Resource):

    def post(self):
        json_data = request.get_json()
        if self.json_validator.validate_data(json_data):
            self.recv_callback(json_data)
            return "OK", 200
        else:
            return "Bad Request", 400


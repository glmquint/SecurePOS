from flask import request
from flask_restful import Resource, Api
from src.JsonIO.JsonValidator import JSONValidator


class FileEndpoint(Resource):

    def __init__(self, **kwargs):
        self.recv_callback = kwargs['recv_callback']

    def post(self, **kwargs):
        print(request.files)
        file = request.files['uploaded']
        if file.filename == '':
            return "Expected file", 460
        self.recv_callback(file)
        return "OK", 200

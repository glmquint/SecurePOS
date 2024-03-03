from pandas import read_csv
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        data = "ciao"
        return {'data': data}, 200
    def post(self):
        some_json = request.get_json()
        return {'you sent ': some_json}, 201

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
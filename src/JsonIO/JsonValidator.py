import json

import jsonschema
from jsonschema import validate, ValidationError, Draft7Validator

class JSONValidator:
    def __init__(self, schema_file):
        with open(schema_file, 'r') as f:
            self.schema = json.load(f)
    def validate_data(self, data):
        try:
            jsonschema.validate(instance=data, schema=self.schema)
            print("Validation successful.")
        except jsonschema.exceptions.ValidationError as e:
            raise Exception(e)
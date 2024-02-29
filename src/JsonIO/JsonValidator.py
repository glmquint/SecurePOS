import json

class JSONValidator:
    def __init__(self, schema_path : str):
        self.schema_path = schema_path
        self.schema = self.load_schema(self.schema_path)
        self.validator = Draft7Validator(self.schema)

    def load_schema(self, schema_path : str):
        with open(schema_path, 'r') as schema_file:
            schema = json.load(schema_file)
        return schema

    def validate(self, json_data):
        return self.validator.is_valid(json_data)
import json
import jsonschema

actually_validate = True

class JSONValidator:
    """
        This class is responsible for validating JSON objects against a JSON schema.

        Attributes:
            schema_file: A string containing the path to the JSON schema file.
            schema: A dictionary containing the JSON schema.

        Methods:
            validate_json_string: Validates a JSON string against the JSON schema.
            validate_data: Validates a JSON object against the JSON schema.
    """
    def __init__(self, schema_file):
        self.schema_file = schema_file  # used for debugging
        with open(schema_file, 'r') as f:
            self.schema = json.load(f)

    def validate_json_string(self, json_string):
        data = json.loads(json_string)
        self.validate_data(data)

    def validate_data(self, data):
        if not actually_validate:
            # print("Validation skipped.", __file__)
            return
        try:
            jsonschema.validate(instance=data, schema=self.schema)
            # print("Validation successful.")
        except jsonschema.exceptions.ValidationError as e:
            raise Exception(e)

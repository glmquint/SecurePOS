import json
from jsonschema import validate, ValidationError, Draft7Validator

#TODO eliminare i vari return
class JSONValidator:
    def __init__(self, schema_file):
        return
        with open(schema_file, 'r') as f:
            self.schema = json.load(f)

    def validate_json_string(self, json_string):
        return
        data = json.loads(json_string)
        self.validate_data(data)

    def validate_data(self, data):
        return
        validator = Draft7Validator(self.schema)
        errors = list(validator.iter_errors(data))
        if errors:
            error_messages = "\n".join(errors)
            raise ValidationError(error_messages)
        else:
            print("Validation successful")

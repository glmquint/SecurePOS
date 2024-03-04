import json

import jsonschema

actually_validate = True

class JSONValidator:
    def __init__(self, schema_file):
        with open(schema_file, 'r') as f:
            self.schema = json.load(f)
    def validate_data(self, data):
        try:
            if not actually_validate:
                print("Validation skipped.", __file__)
                return
            jsonschema.validate(instance=data, schema=self.schema)
            print("Validation successful.")
        except jsonschema.exceptions.ValidationError as e:
            raise Exception(e)

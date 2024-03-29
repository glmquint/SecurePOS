import unittest
import json
from jsonschema import ValidationError

from src.JsonIO.JsonValidator import JSONValidator


# Import JSONValidator class here

class TestJSONValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Write the schema to a file
        schema = {
            "type": "object",
            "properties": {
                "attackRiskLabel": {
                    "type": "string",
                    "enum": ["low", "medium", "high"]
                }
            },
            "required": ["attackRiskLabel"]
        }
        with open("schema.json", "w") as f:
            json.dump(schema, f)

    def setUp(self):
        self.validator = JSONValidator("schema.json")

    def test_valid_json(self):
        valid_data = {
            "attackRiskLabel": "low"
        }
        # Ensure that validation succeeds for the valid JSON data
        self.assertIsNone(self.validator.validate_data(valid_data))

    def test_invalid_json_wrong_label_value(self):
        invalid_data = {
            "attackRiskLabel": "critical"
        }
        # Ensure that validation fails for the invalid JSON data and
        # ValidationError is raised
        with self.assertRaises(ValidationError):
            self.validator.validate_data(invalid_data)

    def test_invalid_json_wrong_label_name(self):
        invalid_data = {
            "RiskLabel": "medium"
        }
        # Ensure that validation fails for the invalid JSON data and
        # ValidationError is raised
        with self.assertRaises(ValidationError):
            self.validator.validate_data(invalid_data)

    @classmethod
    def tearDownClass(cls):
        import os
        os.remove("schema.json")


if __name__ == '__main__':
    unittest.main()

import requests

from src.JsonIO.JsonValidator import JSONValidator


class JSONSender:
    def __init__(self, json_schema_path : str, url : str):
        self.json_schema_path = json_schema_path
        self.url = url
        if json_schema_path != "":
            self.validator = JSONValidator(json_schema_path)

    def send(self, obj):
        try:
            if self.json_schema_path != "":
                self.validator.validate_data(obj)
            requests.post(self.url, json=obj)
        except Exception as e:
            print(e)
            return False
        return True


import requests

from src.JsonIO.JsonValidator import JSONValidator
from src.util import log


class JSONSender:
    def __init__(self, json_schema_path : str, url : str):
        self.json_schema_path = json_schema_path
        self.url = url
        self.validator = JSONValidator(json_schema_path)

    @log
    def send(self, obj):
        try:
            self.validator.validate_data(obj)
            requests.post(self.url, json=obj.to_json())
        except Exception as e:
            print(e, f"({__file__})")
            return False
        return True
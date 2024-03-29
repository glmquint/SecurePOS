import requests
from src.JsonIO.JsonValidator import JSONValidator
from src.util import log


class JSONSender:
    """
        This class is responsible for sending JSON objects to a specified URL.

        Attributes:
            json_schema_path: A string containing the path to the JSON schema file.
            url: A string containing the URL to which the JSON object should be sent.
            validator: A JSONValidator object that is used to validate the JSON object.

        Methods:
            send: Sends a JSON object to the specified URL. It sends a POST request with the JSON object as a parameter.
            If the request fails, it prints the error and returns False. Otherwise, it returns True.
    """
    def __init__(self, json_schema_path: str, url: str) -> None:
        self.json_schema_path = json_schema_path
        self.url = url
        self.validator = JSONValidator(json_schema_path)

    def send(self, obj):
        try:
            self.validator.validate_data(obj.to_json())
            requests.post(self.url, json=obj.to_json())
        except Exception as e:
            print(e, f"({__file__})")
            with open("error.log", "a") as f:
                f.write(f"{e} ({__file__})\n")
            raise e
        return True

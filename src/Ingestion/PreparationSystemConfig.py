import json

from src.JsonIO.JsonValidator import JSONValidator


class PreparationSystemConfig:
    def __init__(self, schema_path:str):
        self.preparation_sys_receiver = None
        self.prepared_session_creator = None
        self.raw_session_creator = None
        self.phase_tracker = None
        self.raw_session_topic = None
        self.db = None
        self.validator = JSONValidator(schema_path)

    def init_from_json(self, json_data:dict):
        self.validator.validate_data(json_data)
        self.__dict__ = json_data

    def init_from_file(self, file_path:str):
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.init_from_json(data)
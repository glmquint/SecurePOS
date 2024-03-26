import json
import os

from src.JsonIO.JsonValidator import JSONValidator


class PreparationSystemConfig:
    def __init__(self, config_path:str, schema_path:str = f"{os.path.dirname(__file__)}/../DataObjects/Schema/PreparationSystemConfigSchema.json"):
        self.ingestion_sys_sender = None
        self.preparation_sys_receiver = None
        self.prepared_session_creator = None
        self.raw_session_creator = None
        self.phase_tracker = None
        self.raw_session_topic = None
        self.db = None
        self.validator = JSONValidator(schema_path)
        with open(config_path, 'r') as f:
            data = json.load(f)
            self.init_from_json(data)

    def init_from_json(self, json_data:dict):
        self.validator.validate_data(json_data)
        self.__dict__ = json_data

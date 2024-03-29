import json
import os

from src.JsonIO.JsonValidator import JSONValidator


class PreparationSystemConfig:
    """
    This class is responsible for managing the configuration of the preparation system.

    The PreparationSystemConfig class initializes various components such as the ingestion system sender,
    preparation system receiver, prepared session creator, raw session creator, and phase tracker.
    It also manages the raw session topic and the database. The configuration is validated against a JSON schema.

    Attributes:
        ingestion_sys_sender (str): Configuration for the ingestion system sender.
        preparation_sys_receiver (str): Configuration for the preparation system receiver.
        prepared_session_creator (str): Configuration for the prepared session creator.
        raw_session_creator (str): Configuration for the raw session creator.
        phase_tracker (str): Configuration for the phase tracker.
        raw_session_topic (str): Topic for raw sessions in the message bus.
        db (str): Configuration for the database.
        validator (JSONValidator): Validates the configuration against a JSON schema.

    Methods:
        init_from_json(json_data): Initializes the configuration from a JSON object.
    """
    def __init__(
            self,
            config_path: str,
            schema_path: str = f"{os.path.dirname(__file__)}/../DataObjects/Schema/PreparationSystemConfigSchema.json"):
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

    def init_from_json(self, json_data: dict):
        self.validator.validate_data(json_data)
        self.__dict__ = json_data

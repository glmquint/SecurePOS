import json


class PreparationSystemConfig:
    def init_from_param(self, config:dict) -> None:
        self.config = config
    def init_from_file(self, config_path:str = "IngestionConfig.json") -> None:
        with open(config_path, "r") as f:
            self.config = json.load(f)


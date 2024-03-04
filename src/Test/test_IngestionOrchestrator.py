from threading import Thread
from time import sleep

import requests

from src.DataObjects.Record import Record
from src.Ingestion.PreparationSystemConfig import PreparationSystemConfig
from src.Ingestion.IngestionOrchestrator import PreparationSystemOrchestrator

DATAOBJ_PATH = "../DataObjects/Schema"

class TestPreparationSystemOrchestrator:
    def test_run(self):
        config = PreparationSystemConfig(f"{DATAOBJ_PATH}/PreparationSystemConfigSchema.json")
        config.init_from_file("PreparationSystemConfig.json")
        orchestrator = PreparationSystemOrchestrator(config)
        Thread(target=orchestrator.run, daemon=True).start()
        record = Record()
        r = requests.post("http://127.0.0.1:5000/record", json=record.__dict__)
        assert r.status_code == 200
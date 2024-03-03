from threading import Thread

from src.DataObjects.Session import RawSession
from src.Ingestion.PhaseTracker import PhaseTracker
from src.Ingestion.PreparationSysReceiver import PreparationSysReceiver
from src.Ingestion.PreparationSystemConfig import PreparationSystemConfig
from src.Ingestion.PreparedSessionCreator import PreparedSessionCreator
from src.Ingestion.RawSessionCreator import RawSessionCreator
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController

class PreparationSystemOrchestrator:
    def __init__(self, config:PreparationSystemConfig) -> None:
        self.config = config
        self.storage_controller = StorageController(dbConfig={"name": "raw_session", "columns": ["device_src", "samples"], "tableName":"raw_session"}, type=type(RawSession))
        self.message_bus = MessageBus(topics=["RawSession"])
        self.phase_tracker = PhaseTracker()
        self.raw_session_creator = RawSessionCreator(self.storage_controller, self.phase_tracker)
        self.prepared_session_creator = PreparedSessionCreator(self.message_bus, self.phase_tracker)
        self.preparation_sys_receiver = PreparationSysReceiver(self.storage_controller, self.message_bus)

    def run(self):
        Thread(target=self.raw_session_creator.run).start()
        Thread(target=self.prepared_session_creator.run).start()
        Thread(target=self.preparation_sys_receiver.run).start()

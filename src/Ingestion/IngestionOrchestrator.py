from src.Ingestion.PhaseTracker import PhaseTracker
from src.Ingestion.PreparationSysReceiver import PreparationSysReceiver
from src.Ingestion.PreparationSystemConfig import PreparationSystemConfig
from src.Ingestion.PreparedSessionCreator import PreparedSessionCreator
from src.Ingestion.RawSessionCreator import RawSessionCreator
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController

class PreparationSystemOrchestrator
    def __init__(self):
        self.config = PreparationSystemConfig()
        self.raw_session_creator = RawSessionCreator()
        self.prepared_session_creator = PreparedSessionCreator()
        self.phase_tracker = PhaseTracker()
        self.storage_controller = StorageController()
        self.preparation_sys_receiver = PreparationSysReceiver()
        self.message_bus = MessageBus()

    def run(self):
        self.prepared_session_creator.run()
        self.phase_tracker.run()
        self.storage_controller.run()
        self.preparation_sys_receiver.run()
        self.message_bus.run()
        self.raw_session_creator.run()

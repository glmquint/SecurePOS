from threading import Thread

from src.DataObjects.Record import Record
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
        self.storage_controller = StorageController(
            dbConfig=self.config.db,
            type=Record)
        self.message_bus = MessageBus(
            topics=[self.config.raw_session_topic])
        self.phase_tracker = PhaseTracker(
            config=self.config.phase_tracker)
        self.raw_session_creator = RawSessionCreator(
            config=self.config.raw_session_creator,
            storage_controller=self.storage_controller,
            phase_tracker=self.phase_tracker)
        self.prepared_session_creator = PreparedSessionCreator(
            config=self.config.prepared_session_creator,
            message_bus=self.message_bus,
            raw_session_topic=self.config.raw_session_topic,
            phase_tracker=self.phase_tracker)
        self.preparation_sys_receiver = PreparationSysReceiver(
            raw_session_topic=self.config.raw_session_topic,
            storage_controller=self.storage_controller,
            message_bus=self.message_bus)

    def run(self) -> None:
        Thread(target=self.preparation_sys_receiver.run).start()
        while True:
            while not self.raw_session_creator.run():
                pass
            self.prepared_session_creator.run()


import os
from threading import Thread

from src.DataObjects.Record import Record
from src.Ingestion.IngestionSystemSender import IngestionSystemSender
from src.Ingestion.PhaseTracker import PhaseTracker
from src.Ingestion.PreparationSysReceiver import PreparationSysReceiver
from src.Ingestion.PreparationSystemConfig import PreparationSystemConfig
from src.Ingestion.PreparedSessionCreator import PreparedSessionCreator
from src.Ingestion.RawSessionCreator import RawSessionCreator
from src.MessageBus.MessageBus import MessageBus
from src.Storage.StorageController import StorageController


class PreparationSystemOrchestrator:
    """
    This class orchestrates the ingestion process by initializing and running various components.

    The PreparationSystemOrchestrator class initializes components such as the StorageController,
    MessageBus, PhaseTracker, IngestionSystemSender, PreparationSysReceiver, RawSessionCreator, and
    PreparedSessionCreator. These components are used to manage the ingestion process, including receiving
    data, creating raw and prepared sessions, and sending data.

    The orchestrator runs these components in separate threads to allow for concurrent processing.

    Attributes:
        config (PreparationSystemConfig): Configuration for the preparation system.
        storage_controller (StorageController): Manages storage-related operations.
        message_bus (MessageBus): Facilitates communication between different components.
        phase_tracker (PhaseTracker): Tracks the phase of the ingestion process.
        ingestion_system_sender (IngestionSystemSender): Sends data to the ingestion system.
        preparation_sys_receiver (PreparationSysReceiver): Receives data from the preparation system.
        raw_session_creator (RawSessionCreator): Creates raw sessions.
        prepared_session_creator (PreparedSessionCreator): Creates prepared sessions.

    Methods:
        run(): Starts the ingestion process by running the PreparationSysReceiver, RawSessionCreator,
               and PreparedSessionCreator in separate threads.
    """
    def __init__(self, config: PreparationSystemConfig = None) -> None:
        if not config:
            config = PreparationSystemConfig(
                config_path=f"{os.path.dirname(__file__)}/config/PreparationSystemConfig.json")
        self.config = config
        self.config.db.update({'buffer_size': 5})
        self.storage_controller = StorageController(
            dbConfig=self.config.db,
            obj_type=Record,
            buffer_size=100
        )
        self.message_bus = MessageBus(
            topics=[self.config.raw_session_topic]
        )
        self.phase_tracker = PhaseTracker(
            config=self.config.phase_tracker
        )
        self.ingestion_system_sender = IngestionSystemSender(
            config=self.config.ingestion_sys_sender,
            is_dev_phase=self.phase_tracker.isDevPhase()
        )
        self.preparation_sys_receiver = PreparationSysReceiver(
            config=self.config.preparation_sys_receiver,
            raw_session_topic=self.config.raw_session_topic,
            storage_controller=self.storage_controller,
            message_bus=self.message_bus
        )
        self.raw_session_creator = RawSessionCreator(
            config=self.config.raw_session_creator,
            storage_controller=self.storage_controller,
            phase_tracker=self.phase_tracker,
            sender=self.ingestion_system_sender
        )
        self.prepared_session_creator = PreparedSessionCreator(
            config=self.config.prepared_session_creator,
            message_bus=self.message_bus,
            raw_session_topic=self.config.raw_session_topic,
            phase_tracker=self.phase_tracker,
            sender=self.ingestion_system_sender
        )

    def run(self) -> None:
        threads = [
            Thread(target=self.preparation_sys_receiver.run),
            Thread(target=self.raw_session_creator.run),
            Thread(target=self.prepared_session_creator.run),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

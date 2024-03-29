import os

from src.DataObjects.Record import Record, Label
from src.DataObjects.Session import RawSession
from src.Ingestion.IngestionSystemSender import IngestionSystemSender
from src.Ingestion.PhaseTracker import PhaseTracker
from src.Storage.StorageController import StorageController


class RawSessionCreator:
    """
    This class is responsible for creating raw sessions from records.

    The RawSessionCreator class retrieves records from the storage, checks if the number of records is sufficient,
    and creates a raw session. It also marks missing samples and validates the raw session.
    If the raw session is valid, it is sent to the Prepared Session creator

    Attributes:
        label (Label): The label of the raw session.
        number_of_systems (int): The number of systems required for a raw session.
        storage_controller (StorageController): Manages storage-related operations.
        phase_tracker (PhaseTracker): Tracks the phase of the ingestion process.
        ingestion_sys_sender (IngestionSystemSender): Sends raw sessions to the ingestion system.
        max_uuid (str): The UUID with the maximum count of records.
        raw_session (RawSession): The raw session currently being created.
        missing_samples (set): The set of missing samples in the raw session.

    Methods:
        isNumberOfRecordsSufficient(): Checks if the number of records is sufficient for a raw session.
        createRawSession(): Creates a raw session from records.
        markMissingSamples(): Marks missing samples in the raw session.
        isRawSessionValid(): Validates the raw session.
        run(): Continuously creates and sends valid raw sessions to the ingestion system.
    """

    def __init__(
            self,
            config,
            storage_controller: StorageController,
            phase_tracker: PhaseTracker,
            sender: IngestionSystemSender) -> None:
        self.label = None
        self.number_of_systems = config['number_of_systems']
        self.storage_controller = storage_controller
        self.phase_tracker = phase_tracker
        self.ingestion_sys_sender = sender

    def isNumberOfRecordsSufficient(self) -> bool:
        uuid_with_max_count = self.storage_controller.isNumberOfRecordsSufficient()
        if len(uuid_with_max_count) == 0:
            return False
        self.max_uuid = uuid_with_max_count[0][0]
        return uuid_with_max_count[0][1] >= self.number_of_systems

    def createRawSession(self) -> None:
        rows_with_max_count = self.storage_controller.retrieve_by_column(
            'uuid', self.max_uuid)
        self.raw_session = RawSession(
            records=[
                Record.from_row(
                    **x) for x in rows_with_max_count])
        assert self.raw_session is not None
        assert len(self.raw_session.records) > 0
        label_records = [
            x for x in self.raw_session.records if isinstance(
                x, Label)]
        self.label = label_records[-1] if len(label_records) > 0 else None

    def markMissingSamples(self) -> None:
        if self.raw_session is None:
            return
        self.missing_samples = set()
        for record in self.raw_session.records:
            self.missing_samples.update(record.get_missing_samples())

    def isRawSessionValid(self) -> bool:
        if self.phase_tracker.isEvalPhase() and self.label is None:
            return False
        return all(  # all missing samples ...
            [any(  # ... should have at least one valid sample ...
                # ... across all records in the raw session
                [r.__dict__.get(x, None) for r in self.raw_session.records]
            ) for x in self.missing_samples]
        )

    def run(self):
        while True:
            print(f"[{self.__class__.__name__}] Waiting for records")
            while not self.isNumberOfRecordsSufficient():
                pass
            print(f"[{self.__class__.__name__}] Found enough records")
            self.createRawSession()
            self.storage_controller.remove_by_column('uuid', self.max_uuid)
            self.markMissingSamples()
            if not self.isRawSessionValid():
                continue
            if self.phase_tracker.isEvalPhase():
                self.ingestion_sys_sender.send_label(self.label)
            self.ingestion_sys_sender.send_raw_session(self.raw_session)
            self.phase_tracker.increment()

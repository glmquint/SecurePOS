import os

from src.DataObjects.Record import Record, Label
from src.DataObjects.Session import RawSession
from src.Ingestion.IngestionSystemSender import IngestionSystemSender
from src.Ingestion.PhaseTracker import PhaseTracker
from src.JsonIO.JSONSender import JSONSender
from src.Storage.StorageController import StorageController
from src.util import log

class RawSessionCreator:

    def __init__(self, config, storage_controller: StorageController, phase_tracker: PhaseTracker,
                 sender : IngestionSystemSender) -> None:
        self.label                  = None
        self.number_of_systems      = config['number_of_systems']
        self.storage_controller     = storage_controller
        self.phase_tracker          = phase_tracker
        self.ingestion_sys_sender   = sender

    def isNumberOfRecordsSufficient(self) -> bool:
        uuid_with_max_count = self.storage_controller.isNumberOfRecordsSufficient()
        if len(uuid_with_max_count) == 0:
            return False
        self.max_uuid = uuid_with_max_count[0][0]
        return uuid_with_max_count[0][1] >= self.number_of_systems

    def createRawSession(self) -> None:
        rows_with_max_count = self.storage_controller.retrieve_by_column('uuid', self.max_uuid)
        self.raw_session = RawSession(records = [Record.from_row(**x) for x in rows_with_max_count])
        assert self.raw_session is not None
        assert len(self.raw_session.records) > 0
        label_records = [x for x in self.raw_session.records if type(x) == Label]
        self.label = label_records[-1] if len(label_records) > 0 else None

    def markMissingSamples(self) -> None:
        if self.raw_session is None:
            return
        self.missing_samples = set()
        for record in self.raw_session.records:
            self.missing_samples.update(record.getMissingSamples())

    def isRawSessionValid(self) -> bool:
        if self.phase_tracker.isEvalPhase() and self.label is None:
            return False
        return all( # all missing samples ...
            [any( # ... should have at least one valid sample ...
                [r.__dict__.get(x, None) for r in self.raw_session.records] # ... across all records in the raw session
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


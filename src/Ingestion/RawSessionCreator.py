from src.DataObjects.Record import Record
from src.DataObjects.Session import RawSession
from src.Ingestion.PhaseTracker import PhaseTracker
from src.JsonIO.JSONSender import JSONSender
from src.Storage.StorageController import StorageController
from src.util import log

DATAOBJ_PATH = "../DataObjects/Schema"

class RawSessionCreator:

    def __init__(self, config, storage_controller:StorageController, phase_tracker:PhaseTracker) -> None:
        self.sufficient_number_of_records = config['sufficient_number_of_records']
        self.label_sender = JSONSender(f"{DATAOBJ_PATH}/AttackRiskLabelSchema.json", "http://127.0.0.1:8000/label")
        self.raw_session_sender = JSONSender(f"{DATAOBJ_PATH}/RawSessionSchema.json", "http://127.0.0.1:8000/raw_session")
        self.storage_controller = storage_controller
        self.phase_tracker = phase_tracker

    @log
    def retrieveRecords(self) -> [Record]:
        pass

    @log
    def isNumberOfRecordsSufficient(self) -> bool:
        return self.storage_controller.count() >= self.sufficient_number_of_records

    @log
    def createRawSession(self) -> None:
        records = self.storage_controller.retrieve_all()
        self.raw_session = RawSession()
        self.raw_session.records = records

    @log
    def markMissingSamples(self) -> None:
        if self.raw_session is None:
            return
        self.missing_samples = [record for record in self.raw_session.records if record.isMissingSample()]

    @log
    def isRawSessionValid(self) -> bool:
        return len(self.missing_samples) == 0

    @log
    def run(self) -> None:
        while not self.isNumberOfRecordsSufficient():
            pass
        self.createRawSession()
        self.storage_controller.remove_all()
        self.markMissingSamples()
        if self.isRawSessionValid():
            if self.phase_tracker.isEvalPhase():
                self.label_sender.send(self.label)
            self.raw_session_sender.send(self.raw_session)


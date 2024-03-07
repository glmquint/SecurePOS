from src.DataObjects.Record import Record
from src.DataObjects.Session import RawSession
from src.Ingestion.PhaseTracker import PhaseTracker
from src.JsonIO.JSONSender import JSONSender
from src.Storage.StorageController import StorageController
from src.util import log

DATAOBJ_PATH = "../DataObjects/Schema"

class RawSessionCreator:

    def __init__(self, config, storage_controller:StorageController, phase_tracker:PhaseTracker) -> None:
        self.label = None
        self.sufficient_number_of_records = config['sufficient_number_of_records']
        self.label_sender = JSONSender(f"{DATAOBJ_PATH}/AttackRiskLabelSchema.json", config['label_receiver']['url'])
        self.raw_session_sender = JSONSender(f"{DATAOBJ_PATH}/RawSessionSchema.json", config['raw_session_receiver']['url'])
        self.storage_controller = storage_controller
        self.phase_tracker = phase_tracker

    def retrieveRecords(self) -> [Record]:
        pass

    def isNumberOfRecordsSufficient(self) -> bool:
        if self.phase_tracker.isDevPhase(): # nocheckin
            return self.storage_controller.count() >= 1
        return self.storage_controller.count() >= self.sufficient_number_of_records

    def createRawSession(self) -> None:
        records = self.storage_controller.retrieve_all()
        self.raw_session = RawSession()
        self.raw_session.records = records

    def markMissingSamples(self) -> None:
        if self.raw_session is None:
            return
        self.missing_samples = [record for record in self.raw_session.records if record.isMissingSample()]

    def isRawSessionValid(self) -> bool:
        if self.phase_tracker.isDevPhase(): # nocheckin
            return True
        return len(self.missing_samples) == 0

    def run(self) -> bool:
        while not self.isNumberOfRecordsSufficient():
            pass
        self.createRawSession()
        self.storage_controller.remove_all()
        self.markMissingSamples()
        if not self.isRawSessionValid():
            return False
        if self.phase_tracker.isEvalPhase():
            self.label_sender.send(self.label)
        self.raw_session_sender.send(self.raw_session)
        return True


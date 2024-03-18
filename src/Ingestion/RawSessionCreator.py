from src.DataObjects.Record import Record
from src.DataObjects.RecordOld import RecordOld
from src.DataObjects.Session import RawSession
from src.Ingestion.PhaseTracker import PhaseTracker
from src.JsonIO.JSONSender import JSONSender
from src.Storage.StorageController import StorageController
from src.util import log

DATAOBJ_PATH = "../DataObjects/Schema"

class RawSessionCreator:

    def __init__(self, config, storage_controller:StorageController, phase_tracker:PhaseTracker) -> None:
        self.label              = None
        self.number_of_systems  = config['number_of_systems']
        self.label_sender       = JSONSender(f"{DATAOBJ_PATH}/AttackRiskLabelSchema.json", config['label_receiver']['url'])
        self.raw_session_sender = JSONSender(f"{DATAOBJ_PATH}/RawSessionSchema.json", config['raw_session_receiver']['url'])
        self.storage_controller = storage_controller
        self.phase_tracker      = phase_tracker

    def retrieveRecords(self) -> [RecordOld]:
        pass

    def isNumberOfRecordsSufficient(self) -> bool:
        uuid_with_max_count = self.storage_controller.executeQuery("select uuid, count(distinct(objtype)) as different_systems from record group by uuid order by different_systems desc limit 1;")
        if len(uuid_with_max_count) == 0:
            return False
        self.max_uuid = uuid_with_max_count[0][0]
        return uuid_with_max_count[0][1] >= self.number_of_systems

    def createRawSession(self) -> None:
        rows_with_max_count = self.storage_controller.retrieve_by_column('uuid', self.max_uuid)
        self.raw_session = RawSession(records = [Record.from_row(**x) for x in rows_with_max_count])

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
            while not self.isNumberOfRecordsSufficient():
                pass
            self.createRawSession()
            self.storage_controller.remove_by_column('uuid', self.max_uuid)
            self.markMissingSamples()
            if not self.isRawSessionValid():
                continue
            if self.phase_tracker.isEvalPhase():
                self.label_sender.send(self.label)
            self.raw_session_sender.send(self.raw_session)
            continue

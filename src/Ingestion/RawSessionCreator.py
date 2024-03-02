from src.DataObjects.Record import Record
from src.JsonIO.JSONSender import JSONSender

DATAOBJ_PATH = "/src/DataObjects/Schema"

class RawSessionCreator:

    def __init__(self, storage_controller, phase_tracker):
        self.sufficient_number_of_records = 100
        self.label_sender = JSONSender(f"{DATAOBJ_PATH}/labels.json", "http://127.0.0.1:8000/label")
        self.raw_session_sender = JSONSender(f"{DATAOBJ_PATH}/raw_session.json", "http://127.0.0.1:8000/raw_session")
        self.storage_controller = storage_controller
        self.phase_tracker = phase_tracker

    def retrieveRecords(self) -> [Record]:
        pass

    def isNumberOfRecordsSufficient(self) -> bool:
        return self.storage_controller.count() > self.sufficient_number_of_records

    def createRawSession(self, records:[Record]) -> None:
        pass

    def markMissingSamples(self, raw_session:RawSession) -> None:
        pass

    def isRawSessionValid(self, raw_session:RawSession) -> bool:
        pass

    def run(self) -> None:
        while True:
            if self.isNumberOfRecordsSufficient():
                self.createRawSession()
                self.storage_controller.remove()
                self.markMissingSamples()
                if self.isRawSessionValid():
                    if self.phase_tracker.isEvalPhase():
                        self.label_sender.send(self.label)
                    self.raw_session_sender.send(self.raw_session)


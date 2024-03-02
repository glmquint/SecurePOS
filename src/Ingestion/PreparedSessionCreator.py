from src.DataObjects.Session import RawSession
from src.Ingestion.PhaseTracker import PhaseTracker
from src.JsonIO.JSONSender import JSONSender
from src.MessageBus.MessageBus import MessageBus

DATAOBJ_PATH = "/src/DataObjects/Schema"

class PreparedSessionCreator:
    def __init__(self, message_bus:MessageBus, phase_tracker:PhaseTracker) -> None:
        self.message_bus : MessageBus = message_bus
        self.phase_tracker : PhaseTracker = phase_tracker
        self.prepared_session_sender : JSONSender = JSONSender(f"{DATAOBJ_PATH}/prepared_session.json", "http://127.0.0.1:8000/prepared_session")
        self.raw_session : RawSession = None

    def run(self) -> None:
        while True:
            self.raw_session : RawSession = self.message_bus.popTopic("RawSession")
            self.correctMissingSamples()
            self.detectAndCorrectAbsoluteOutliers()
            self.exrtactFeatures()
            if self.phase_tracker.isDevPhase():
                self.prepared_session_sender.sendToSegregationSys(self.raw_session)
            else:
                self.prepared_session_sender.sendToProductionSys(self.raw_session)

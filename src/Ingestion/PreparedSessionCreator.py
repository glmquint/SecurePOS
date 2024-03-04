from src.DataObjects.Session import RawSession
from src.Ingestion.PhaseTracker import PhaseTracker
from src.JsonIO.JSONSender import JSONSender
from src.MessageBus.MessageBus import MessageBus

DATAOBJ_PATH = "../DataObjects/Schema"

class PreparedSessionCreator:
    def __init__(self, message_bus:MessageBus, raw_session_topic:str, phase_tracker:PhaseTracker) -> None:
        self.message_bus : MessageBus = message_bus
        self.raw_session_topic : str = raw_session_topic
        self.phase_tracker : PhaseTracker = phase_tracker
        self.prepared_session_sender : JSONSender = JSONSender(f"{DATAOBJ_PATH}/PreparedSessionSchema.json", "http://127.0.0.1:8000/prepared_session")
        self.raw_session : RawSession = None

    def run(self) -> None:
        self.raw_session : RawSession = self.message_bus.popTopic(self.raw_session_topic)
        self.correctMissingSamples()
        self.detectAndCorrectAbsoluteOutliers()
        self.exrtactFeatures()
        if self.phase_tracker.isDevPhase():
            self.prepared_session_sender.sendToSegregationSys(self.raw_session)
        else:
            self.prepared_session_sender.sendToProductionSys(self.raw_session)

from src.DataObjects.Session import RawSession
from src.Ingestion.PhaseTracker import PhaseTracker
from src.JsonIO.JSONSender import JSONSender
from src.MessageBus.MessageBus import MessageBus
from src.util import log

DATAOBJ_PATH = "../DataObjects/Schema"

class PreparedSessionCreator:
    def __init__(self, config , message_bus:MessageBus, raw_session_topic:str, phase_tracker:PhaseTracker) -> None:
        self.config = config
        self.message_bus : MessageBus = message_bus
        self.raw_session_topic : str = raw_session_topic
        self.phase_tracker : PhaseTracker = phase_tracker
        if self.phase_tracker.isDevPhase():
            self.prepared_session_sender : JSONSender = JSONSender(f"{DATAOBJ_PATH}/PreparedSessionSchema.json", self.config["segregation_system_receiver"]["url"])
        else:
            self.prepared_session_sender : JSONSender = JSONSender(f"{DATAOBJ_PATH}/PreparedSessionSchema.json", self.config["production_system_receiver"]["url"])
        self.raw_session : RawSession = None

    def run(self) -> None:
        while True:
            self.raw_session : RawSession = self.message_bus.popTopic(self.raw_session_topic)
            self.correctMissingSamples()
            self.detectAndCorrectAbsoluteOutliers()
            self.exrtactFeatures()
            if self.phase_tracker.isDevPhase():
                self.prepared_session_sender.send(self.raw_session)
            else:
                self.prepared_session_sender.send(self.raw_session)

    def correctMissingSamples(self):
        pass

    def detectAndCorrectAbsoluteOutliers(self):
        pass

    def exrtactFeatures(self):
        pass

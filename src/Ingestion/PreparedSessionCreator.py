import statistics
from timeit import timeit

from src.DataObjects.Session import RawSession
from src.Ingestion.PhaseTracker import PhaseTracker
from src.JsonIO.JSONSender import JSONSender
from src.MessageBus.MessageBus import MessageBus
from src.util import log

DATAOBJ_PATH = "../DataObjects/Schema"

class PreparedSessionCreator:
    def __init__(self, config , message_bus:MessageBus, raw_session_topic:str, phase_tracker:PhaseTracker) -> None:
        self.config                       = config
        self.message_bus : MessageBus     = message_bus
        self.raw_session_topic : str      = raw_session_topic
        self.phase_tracker : PhaseTracker = phase_tracker
        # dev/prod phase doesn't change during execution. We switch between segregation_sys and production_sys only once
        self.prepared_session_sender : JSONSender = JSONSender(f"{DATAOBJ_PATH}/PreparedSessionSchema.json", self.config["segregation_system_receiver" if self.phase_tracker.isDevPhase() else "production_system_receiver"]["url"])
        self.raw_session : RawSession = None

    def run(self) -> None:
        while True:
            self.raw_session : RawSession = self.message_bus.popTopic(self.raw_session_topic)
            self.correctMissingSamples()
            self.detectAndCorrectAbsoluteOutliers()
            self.extractFeatures()
            self.prepared_session_sender.send(self.raw_session)

    @log
    def correctMissingSamples(self):
        pass

    @log
    def detectAndCorrectAbsoluteOutliers(self):
        pass

    @log
    def extractFeatures(self):
        # TODO: process ip as integer for mlpclassification, like -> int(ipaddress.ip_address(schifo.ip)
        pass

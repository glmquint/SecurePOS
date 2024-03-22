import ipaddress
import statistics
from timeit import timeit

from src.DataObjects.Record import TransactionCloudRecord, LocalizationSysRecord, NetworkMonitorRecord, Label
from src.DataObjects.Session import RawSession, PreparedSession
from src.Ingestion.PhaseTracker import PhaseTracker
from src.JsonIO.JSONSender import JSONSender
from src.MessageBus.MessageBus import MessageBus
from src.util import log

DATAOBJ_PATH = "../DataObjects/Schema"

class PreparedSessionCreator:
    def __init__(self, config , message_bus:MessageBus, raw_session_topic:str, phase_tracker:PhaseTracker) -> None:
        self.config                                         = config
        self.message_bus               : MessageBus         = message_bus
        self.raw_session_topic         : str                = raw_session_topic
        self.phase_tracker             : PhaseTracker       = phase_tracker
        # dev/prod phase doesn't change during execution. We switch between segregation_sys and production_sys only once
        self.prepared_session_sender   : JSONSender         = JSONSender(f"{DATAOBJ_PATH}/PreparedSessionSchema.json", self.config["segregation_system_receiver" if self.phase_tracker.isDevPhase() else "production_system_receiver"]["url"])
        self.raw_session               : RawSession         = None
        self.prepared_session          : PreparedSession    = None

    def run(self) -> None:
        while True:
            self.raw_session : RawSession = self.message_bus.popTopic(self.raw_session_topic)
            self.correctMissingSamples()
            self.detectAndCorrectAbsoluteOutliers()
            self.extractFeatures()
            if self.prepared_session is not None:
                self.prepared_session_sender.send(self.prepared_session)
            self.prepared_session = None

    @log
    def correctMissingSamples(self):
        for record in self.raw_session.records:
            for key, value in record.getMissingSamples():
                # get the last sample of the same type
                record.__dict__[key] = [x for x in self.raw_session.records if x.__dict__.get(key, None) is not None][-1].__dict__[key]

    @log
    def detectAndCorrectAbsoluteOutliers(self):
        for record in self.raw_session.records:
            for key, value in record.getOutliers().items():
                # set the outlier the nearest upper/lower bound
                record.clamp(key, value)

    @log
    def extractFeatures(self):
        mean_abs_diff_transaction = statistics.mean(
            [statistics.mean([abs(x - y) for x, y in zip(record.timestamp, record.timestamp[1:])]) for record in
             self.raw_session.records if type(record) is TransactionCloudRecord])
        mean_abs_diff_transaction_amount = statistics.mean(
            [statistics.mean([abs(x - y) for x, y in zip(record.amount, record.amount[1:])]) for record in
             self.raw_session.records if type(record) is TransactionCloudRecord])
        longitudes = [record.location_longitude for record in self.raw_session.records if type(record) is LocalizationSysRecord]
        latitudes = [record.location_latitude for record in self.raw_session.records if type(record) is LocalizationSysRecord]
        median_longitude, median_latitude = statistics.median(longitudes), statistics.median(latitudes)
        target_ips = [int(ipaddress.ip_address(record.target_ip)) for record in self.raw_session.records if type(record) is NetworkMonitorRecord]
        dest_ips = [int(ipaddress.ip_address(record.dest_ip)) for record in self.raw_session.records if type(record) is NetworkMonitorRecord]
        median_target_ip = statistics.median(target_ips)
        median_dest_ip = statistics.median(dest_ips)
        labels = [record.label for record in self.raw_session.records if type(record) is Label]
        label = labels[-1] if len(labels) > 0 else None
        self.prepared_session = PreparedSession(uuid=self.raw_session.records[0].uuid, # all records have the same uuid
                                               mean_abs_diff_transaction=mean_abs_diff_transaction,
                                               mean_abs_diff_transaction_amount= mean_abs_diff_transaction_amount,
                                               median_longitude=median_longitude,
                                               median_latitude=median_latitude,
                                               median_target_ip=median_target_ip,
                                               median_dest_ip=median_dest_ip,
                                               label=label)



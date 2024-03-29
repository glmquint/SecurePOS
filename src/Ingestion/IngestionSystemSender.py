import os

from src.JsonIO.JSONSender import JSONSender
from src.util import monitorPerformance

DATAOBJ_PATH = f"{os.path.dirname(__file__)}/../DataObjects/Schema"


class IngestionSystemSender:
    def __init__(self, config: dict, is_dev_phase: bool):
        self.label_sender: JSONSender = JSONSender(
            f"{DATAOBJ_PATH}/Label.json", config['label_receiver']['url'])
        self.raw_session_sender: JSONSender = JSONSender(
            f"{DATAOBJ_PATH}/RawSessionSchema.json",
            config['raw_session_receiver']['url'])
        # dev/prod phase doesn't change during execution. We switch between
        # segregation_sys and production_sys only once
        self.prepared_session_sender: JSONSender = JSONSender(
            f"{DATAOBJ_PATH}/PreparedSessionSchema.json",
            config["segregation_system_receiver"]['url'] if is_dev_phase else config["production_system_receiver"]["url"])

    @monitorPerformance(should_sample_after=True)
    def send_label(self, label):
        self.label_sender.send(label)

    @monitorPerformance(should_sample_after=True)
    def send_raw_session(self, raw_session):
        self.raw_session_sender.send(raw_session)
        assert len(
            raw_session.records) > 0, f"empty records in {raw_session.records}"

    @monitorPerformance(should_sample_after=True)
    def send_prepared_session(self, prepared_session):
        self.prepared_session_sender.send(prepared_session)

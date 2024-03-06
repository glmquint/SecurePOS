from src.JsonIO.JSONSender import JSONSender


class ServiceSender:
    def __init__(self, raw_session):
        self.raw_session = raw_session

    def send(self, url):
        sender = JSONSender("../DataObjects/Schema/RawSessionSchema.json", url)
        sender.send(self.raw_session.to_json())

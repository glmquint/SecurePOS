from src.JsonIO.JSONSender import JSONSender


class DevelopmentSystemSender:
    messaging_sender: JSONSender = None
    production_sender: JSONSender = None

    def __init__(self):
        self.messaging_sender = JSONSender()
        self.production_sender = JSONSender()

    def send_to_messaging(self, Config):
        self.messaging_sender.send(Config)

    def send_to_production(self, Classifier):
        self.production_sender.send(Classifier)

import os
from threading import Thread

import joblib

from src.Ingestion.PhaseTracker import PhaseTracker
from src.MessageBus.MessageBus import MessageBus
from src.Production.AttackRiskClassifier import AttackRiskClassifier
from src.Production.ProductionSystemReceiver import ProductionSystemReceiver
from src.Production.ProductionSystemSender import ProductionSystemSender
from src.Production.ProductionSystemConfig import ProductionSystemConfig
from src.util import Message


class ProductionSystemOrchestrator:
    """
        This class is responsible for orchestrating the production system. It initializes the system configuration,
        phase tracker, message bus, production system receiver, and sender. It also loads the classifier model if
        available.

        Attributes:
            production_config: An object that stores and manages the configuration of the production system.
            phase_tracker: An object that tracks the current phase of the system.
            system_bus: An object that provides access to the system's bus for inter-process communication.
            prod_sys_receiver: An object that receives messages from the server.
            sender: An object that sends messages to the client, evaluation, and messaging URLs.
            classifier: A classifier object used to predict the attack risk label.
        """
    def __init__(self, config: ProductionSystemConfig = None):
        if not config:
            config = ProductionSystemConfig(
                f'{os.path.dirname(__file__)}/config/config.json')
        self.production_config = config
        self.phase_tracker = PhaseTracker(
            {
                "production_phase_duration": self.production_config.monitoring_window,
                "evaluation_phase_duration": self.production_config.evaluation_window,
                "phase": self.production_config.phase
            }
        )
        self.system_bus = MessageBus(["PreparedSession", "Classifier"])
        self.prod_sys_receiver = ProductionSystemReceiver(
            self.production_config.server_port, self.system_bus)
        self.sender = ProductionSystemSender(
            self.production_config.message_url,
            self.production_config.evaluation_url,
            self.production_config.client_url)
        try:
            # The absence of this file means we are in development phase
            self.classifier = joblib.load(
                f"{os.path.dirname(__file__)}/classifier.sav")
            print(f"Classifier loaded {self.classifier}")
        except FileNotFoundError:
            self.classifier = None

    def main(self):
        thread = Thread(target=self.prod_sys_receiver.run)
        # this will allow the main thread to exit even if the server is still
        # running
        thread.daemon = True
        thread.start()
        attack_risk_classifier = AttackRiskClassifier(
            self.system_bus, self.classifier)
        while True:
            # if the classifier.sav is not present try to pop it from the
            # systemBus for synchronisation
            if self.classifier is None:
                self.classifier = self.system_bus.popTopic("Classifier")
                print(f"Classifier {self.classifier}")
                self.sender.sendToMessaging(Message(msg="Classifier received"))
                quit()
            try:
                attack_risk_label = attack_risk_classifier.provideAttackRiskLabel()
                print(type(attack_risk_label))
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

            if self.phase_tracker.isEvalPhase():
                self.sender.sendToEvaluation(attack_risk_label)
                print("Send to evaluation")
            self.sender.sendToClient(attack_risk_label)
            self.phase_tracker.increment()
            print("Send to client")

    def run(self):
        self.main()


if __name__ == "__main__":
    orchestrator = ProductionSystemOrchestrator()
    orchestrator.run()

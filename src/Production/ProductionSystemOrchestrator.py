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

    def __init__(self, config : ProductionSystemConfig = None):
        if not config:
            config = ProductionSystemConfig(f'{os.path.dirname(__file__)}/config/configSchema.json')
        self.productionConfig = config
        self.phaseTracker = PhaseTracker({"production_phase_duration": self.productionConfig.monitoring_window,
                                          "evaluation_phase_duration": self.productionConfig.evaluation_window,
                                          "phase": self.productionConfig.phase})
        self.systemBus = MessageBus(["PreparedSession", "Classifier"])
        self.prodSysRec = ProductionSystemReceiver(self.productionConfig.server_port, self.systemBus)
        self.sender = ProductionSystemSender(self.productionConfig.message_url,
                                             self.productionConfig.evaluation_url,
                                             self.productionConfig.client_url)
        try:
            # The absence of this file means we are in development phase
            self.classifier = joblib.load(f"{os.path.dirname(__file__)}/classifier.sav")
            print(f"Classifier loaded {self.classifier}")
        except FileNotFoundError:
            self.classifier = None

    def main(self):
        thread = Thread(target=self.prodSysRec.run)
        thread.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread.start()
        attackRiskClassifier = AttackRiskClassifier(self.systemBus, self.classifier)
        while True:
            # if the classifier.sav is not present try to pop it from the systemBus for synchronisation
            if self.classifier is None:
                self.classifier = self.systemBus.popTopic("Classifier")
                print(f"Classifier {self.classifier}")
                self.sender.sendToMessaging(Message(msg="Classifier received"))
                quit()
            try:
                attack_risk_label = attackRiskClassifier.provideAttackRiskLabel()
                print(type(attack_risk_label))
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
            # TODO: fix schema for attack_risk_label

            if self.phaseTracker.isEvalPhase():
                #self.sender.sendToEvaluation(attack_risk_label)
                print("Send to evaluation")
            #self.sender.sendToClient(attack_risk_label)
            self.phaseTracker.increment()
            print("Send to client")

    def run(self):
        self.main()


if __name__ == "__main__":
    orchestrator = ProductionSystemOrchestrator()
    orchestrator.run()
import os
from threading import Thread

import joblib

from src.Ingestion.PhaseTracker import PhaseTracker
from src.MessageBus.MessageBus import MessageBus
from src.Production.FakeAttackRiskClassifier import FakeAttackRiskClassifier
from src.Production.ProductionSystemReceiver import ProductionSystemReceiver
from src.Production.ProductionSystemSender import ProductionSystemSender
from src.Production.ProductuinSystemConfig import ProductionSystemConfig
from src.util import Message


class ProductionSystemOrchestrator:

    def __init__(self):
        self.productionConfig = ProductionSystemConfig(f'{os.path.dirname(__file__)}/config/config.json',
                                                       f'{os.path.dirname(__file__)}/config/configSchema.json')
        #self.phaseTracker = ProductionSystemPhaseTracker(self.productionConfig.monitoring_window,
        #                                                 self.productionConfig.evaluation_window)
        self.phaseTracker = PhaseTracker({"production_phase_duration": self.productionConfig.monitoring_window,"evaluation_phase_duration": self.productionConfig.evaluation_window})
        self.systemBus = MessageBus(["PreparedSession", "Classifier"])
        self.prodSysRec = ProductionSystemReceiver(self.productionConfig.server_port, self.systemBus)
        self.sender = ProductionSystemSender(self.productionConfig.message_url,
                                             self.productionConfig.evaluation_url,
                                             self.productionConfig.client_url)
        try:
            self.classifier = joblib.load(f"{os.path.dirname(__file__)}/classifier.sav") # The absence of this file means we are in development phase
            print(f"Classifier loaded {self.classifier}")
        except FileNotFoundError:
            self.classifier = None

    def main(self):
        thread = Thread(target=self.prodSysRec.run)
        thread.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread.start()
        attackRiskClassifier = FakeAttackRiskClassifier(self.systemBus, self.classifier)
        while True:
            # if the classifier.sav is not present try to pop it from the systemBus
            if self.classifier is None:
                self.classifier = self.systemBus.popTopic("Classifier")
                print(f"Classifier {self.classifier}")
                self.sender.sendToMessaging(Message(msg="Classifier received"))
                quit()
            #print(f"Fake classifier classifier pre {fakeClassifier.attackRiskClassifier}")
            attackRiskLabel = attackRiskClassifier.provideAttackRiskLabel()
            print(type(attackRiskLabel))
            #print(f"Fake classifier classifier post {fakeClassifier.attackRiskClassifier}")
            # TODO: fix schema for attackRiskLabel

            if self.phaseTracker.isEvalPhase():
                self.sender.sendToEvaluation(attackRiskLabel)
                print("Send to evaluation")
            self.sender.sendToClient(attackRiskLabel)
            self.phaseTracker.increment()
            print("Send to client")

    def run(self):
        self.main()

if __name__ == "__main__":
    orchestrator = ProductionSystemOrchestrator()
    orchestrator.run()
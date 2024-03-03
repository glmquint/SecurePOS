from threading import Thread

from src.MessageBus.MessageBus import MessageBus
from src.Production.FakeAttackRiskClassifier import FakeAttackRiskClassifier
from src.Production.ProductionSystemPhaseTracker import ProductionSystemPhaseTracker
from src.Production.ProductionSystemReceiver import ProductionSystemReceiver
from src.Production.ProductionSystemSender import ProductionSystemSender
from src.Production.ProductuinSystemConfig import ProductionSystemConfig

class ProductionSystemOrchestrator:
    def main(self):
        # Get an instance of the ProductionSystemConfig
        productionConfig = ProductionSystemConfig()
        phaseTracker = ProductionSystemPhaseTracker(productionConfig.monitoring_window, productionConfig.evaluation_window)
        # Print the configuration
        print(productionConfig)
        # Print the phase tracker
        print(phaseTracker)

        systemBus = MessageBus(["PreparedSession", "Classifier"])

        prodSysRec = ProductionSystemReceiver(systemBus)
        thread = Thread(target=prodSysRec.run)
        thread.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread.start()
        fakeClassifier = FakeAttackRiskClassifier(systemBus)
        while True:
            # classifier = AttackRiskClassifier(systemBus)
            # attackRiskLabel = classifier.provideAttackRiskLabel()
            #print(f"Fake classifier classifier pre {fakeClassifier.attackRiskClassifier}")
            attackRiskLabel = fakeClassifier.provideAttackRiskLabel()
            #print(f"Fake classifier classifier post {fakeClassifier.attackRiskClassifier}")
            phaseTracker.increseCounter()
            sender = ProductionSystemSender(attackRiskLabel)
            if not (phaseTracker.isProduction()):
                sender.send(productionConfig.evaluation_url)
                print("Send to evaluation")
            sender.send(productionConfig.client_url)
            print("Send to client")

    def run(self):
        self.main()

if __name__ == "__main__":
    orchestrator = ProductionSystemOrchestrator()
    orchestrator.run()
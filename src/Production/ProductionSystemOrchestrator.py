from threading import Thread

from src.DataObjects.AttackRiskLabel import AttackRiskLabel
from src.MessageBus.MessageBus import MessageBus
from src.Production.FakeAttackRiskClassifier import FakeAttackRiskClassifier
from src.Production.ProductionSystemPhaseTracker import ProductionSystemPhaseTracker
from src.Production.ProductionSystemReceiver import ProductionSystemReceiver
from src.Production.ProductionSystemSender import ProductionSystemSender
from src.Production.ProductuinSystemConfig import ProductionSystemConfig

class ProductionSystemOrchestrator:

    def __init__(self):
        self.productionConfig = ProductionSystemConfig('./config/config.json', './config/configSchema.json')
        self.phaseTracker = ProductionSystemPhaseTracker(self.productionConfig.monitoring_window,
                                                         self.productionConfig.evaluation_window)
        self.systemBus = MessageBus(["PreparedSession", "Classifier"])
        self.prodSysRec = ProductionSystemReceiver(self.systemBus)
    def main(self):
        thread = Thread(target=self.prodSysRec.run)
        thread.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread.start()
        fakeClassifier = FakeAttackRiskClassifier(self.systemBus)
        while True:
            #print(f"Fake classifier classifier pre {fakeClassifier.attackRiskClassifier}")
            attackRiskLabel = AttackRiskLabel(fakeClassifier.provideAttackRiskLabel())
            print(type(attackRiskLabel))
            #print(f"Fake classifier classifier post {fakeClassifier.attackRiskClassifier}")
            self.phaseTracker.increseCounter()
            sender = ProductionSystemSender(attackRiskLabel)
            if not (self.phaseTracker.isProduction()):
                sender.send(self.productionConfig.evaluation_url)
                print("Send to evaluation")
            sender.send(self.productionConfig.client_url)
            print("Send to client")

    def run(self):
        self.main()

if __name__ == "__main__":
    orchestrator = ProductionSystemOrchestrator()
    orchestrator.run()
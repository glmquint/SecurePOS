from threading import Thread
from src.Production.AttackRiskClassifier import AttackRiskClassifier
from src.Production.ProductionSystemReceiver import ProductionSystemReceiver
from src.Production.ProductionSystemSender import ProductionSystemSender
from src.Production.ProductuinSystemConfig import ProductionSystemConfig
from src.Production.ProductionSystemPhaseTracker import ProductionSystemPhaseTracker
from src.MessageBus.MessageBus import MessageBus
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

while True:
    classifier = AttackRiskClassifier(systemBus)
    attackRiskLabel = classifier.provideAttackRiskLabel()
    phaseTracker.increseCounter()
    sender = ProductionSystemSender(attackRiskLabel)
    if phaseTracker.isProduction():
        sender.send(productionConfig.evaluation_url)
    sender.send(productionConfig.client_url)


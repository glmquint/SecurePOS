import sklearn.neural_network as skl
class AttackRiskClassifier:

    def __init__(self, messageBus):
        self.messageBus = messageBus
        self.attackRiskClassifier = self.loadAttackRiskClassifier()
        self.messageBus.subscribe("PreparedSession", self.onPreparedSession)

    def loadAttackRiskClassifier(self):
        self.classifier = self.messageBus.popTopic("Classifier")

    def loadPreparedSession(self, session):
        self.messageBus.popTopic("PreparedSession")

    def provideAttackRiskLabel(self):
        if self.attackRiskClassifier is None:
            self.loadAttackRiskClassifier()
        return self.attackRiskClassifier.predict(self.loadPreparedSession())



import sklearn.neural_network as skl

from src.DataObjects.AttackRiskLabel import AttackRiskLabel


class FakeAttackRiskClassifier:

    def __init__(self, messageBus):
        self.preparedSession = None
        self.attackRiskClassifier = None
        self.messageBus = messageBus

    def loadAttackRiskClassifier(self):
        return self.messageBus.popTopic("Classifier")

    def loadPreparedSession(self):
        return self.messageBus.popTopic("PreparedSession")

    def provideAttackRiskLabel(self):
        if self.attackRiskClassifier is None:
            print("No classifier")
            self.attackRiskClassifier = self.loadAttackRiskClassifier()
        self.preparedSession = self.loadPreparedSession()
        assert self.preparedSession is not None
        #print(self.preparedSession)
        return AttackRiskLabel("medium")


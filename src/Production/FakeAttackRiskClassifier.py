import sklearn.neural_network as skl

from src.DataObjects.AttackRiskLabel import AttackRiskLabel


class FakeAttackRiskClassifier:

    def __init__(self, systemBus):
        self.systemBus = systemBus
        self.attackRiskClassifier = None

    def provideAttackRiskLabel(self):
        if self.attackRiskClassifier is None:
            self.attackRiskClassifier = self.systemBus.pop("Classifier")
            # assert self.attackRiskClassifier is not None
        self.preparedSession = self.systemBus.pop("PreparedSession")
        # used for debug purpose
        # assert self.preparedSession is not None
        # fake return
        return AttackRiskLabel("medium")


import sklearn.neural_network as skl

from src.DataObjects.AttackRiskLabel import AttackRiskLabel


class FakeAttackRiskClassifier:

    def __init__(self, classifier):
        self.preparedSession = None
        self.attackRiskClassifier = classifier

    def provideAttackRiskLabel(self, preparedSession):
        self.preparedSession = preparedSession
        # used for debug purpose
        # assert self.preparedSession is not None
        # fake return
        return AttackRiskLabel("medium")


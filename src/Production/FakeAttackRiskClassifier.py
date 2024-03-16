import ipaddress

import sklearn.neural_network as skl

from src.DataObjects.AttackRiskLabel import AttackRiskLabel
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

class FakeAttackRiskClassifier:

    def __init__(self, systemBus):
        self.systemBus = systemBus
        self.attackRiskClassifier = None

    def provideAttackRiskLabel(self):
        if self.attackRiskClassifier is None:
            self.attackRiskClassifier = self.systemBus.popTopic("Classifier")
            print(f"Fake classifier classifier {self.attackRiskClassifier}")
            # assert self.attackRiskClassifier is not None
        self.preparedSession = self.systemBus.popTopic("PreparedSession")
        #print(f"Prepared session {self.preparedSession}")
        #print(f"Fake classifier prepared session {self.preparedSession.to_json()}")
        # used for debug purpose
        # assert self.preparedSession is not None
        # fake return
        prepared_session_features = [
            self.preparedSession.MeanAbsoluteDifferencingTransactionTimestamps,
            self.preparedSession.MeanAbsoluteDifferencingTransactionAmount,
            self.preparedSession.MedianLongitude,
            self.preparedSession.MedianLatitude,
            int(ipaddress.ip_address(self.preparedSession.MedianTargetIP)),
            int(ipaddress.ip_address(self.preparedSession.MedianDestIP))
        ]
        print(f"Prepared session features: {prepared_session_features}")
        attack_risk_label = self.attackRiskClassifier.predict([prepared_session_features])[0]
        print(f"Attack risk label: {attack_risk_label}")
        return attack_risk_label


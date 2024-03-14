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
        print(f"Fake classifier prepared session {self.preparedSession}")
        # used for debug purpose
        # assert self.preparedSession is not None
        # fake return
        prepared_session_features = [
            self.preparedSession.mean_absolute_diff_timestamps,
            self.preparedSession.mean_absolute_diff_amount,
            self.preparedSession.median_longitude_latitude[0],
            self.preparedSession.median_longitude_latitude[1],
            # le.transform([prepared_session.median_target_ip]),
            # le.transform([prepared_session.median_dest_ip])
            int(ipaddress.ip_address(self.preparedSession.median_target_ip)),
            int(ipaddress.ip_address(self.preparedSession.median_dest_ip))

            # Add more numeric features here if necessary
        ]
        attack_risk_label = self.attackRiskClassifier.predict([prepared_session_features])[0]
        print(f"Attack risk label: {attack_risk_label}")
        return attack_risk_label


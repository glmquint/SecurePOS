import ipaddress
from uuid import uuid1

import sklearn.neural_network as skl


from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from src.DataObjects.Record import Label


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
        print(f"Prepared session {self.preparedSession}")
        print(f"Fake classifier prepared session {self.preparedSession.to_json()}")
        prepared_session_features = [
            self.preparedSession.mean_abs_diff_transaction,
            self.preparedSession.mean_abs_diff_transaction_amount,
            self.preparedSession.median_longitude,
            self.preparedSession.median_latitude,
            self.preparedSession.median_target_ip,
            self.preparedSession.median_dest_ip
        ]
        print(f"Prepared session features: {prepared_session_features}")
        attack_risk_label = self.attackRiskClassifier.predict([prepared_session_features])[0]
        print(f"Attack risk label: {attack_risk_label}")
        # TODO: add uuid to PreparedSession
        return Label(label=attack_risk_label, uuid=self.preparedSession.uuid)


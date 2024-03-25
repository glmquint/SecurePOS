import ipaddress
from uuid import uuid1

import sklearn.neural_network as skl


from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from src.DataObjects.Record import Label


class AttackRiskClassifier:

    def __init__(self, system_bus, classifier=None):
        self.systemBus = system_bus
        self.attackRiskClassifier = classifier

    def provideAttackRiskLabel(self):
        prepared_session = self.systemBus.popTopic("PreparedSession")
        print(f"Prepared session {prepared_session}")
        print(f"Classifier prepared session {prepared_session.to_json()}")
        prepared_session_features = [
            prepared_session.mean_abs_diff_transaction,
            prepared_session.mean_abs_diff_transaction_amount,
            prepared_session.median_longitude,
            prepared_session.median_latitude,
            prepared_session.median_target_ip,
            prepared_session.median_dest_ip
        ]
        attack_risk_label = self.attackRiskClassifier.predict([prepared_session_features])[0]
        print(f"Attack risk label: {attack_risk_label}")
        return Label(label=attack_risk_label, uuid=prepared_session.uuid)


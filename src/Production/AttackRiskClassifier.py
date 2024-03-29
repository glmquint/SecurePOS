import ipaddress
from uuid import uuid1

import sklearn.neural_network as skl


from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from src.DataObjects.Record import Label


class AttackRiskClassifier:

    def __init__(self, system_bus, classifier=None):
        self.system_bus = system_bus
        self.attack_risk_classifier = classifier

    def provideAttackRiskLabel(self):
        try:
            prepared_session = self.system_bus.popTopic("PreparedSession")
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
        except Exception as e:
            raise Exception(f"An error occurred, wrong data received: {e}")
        try:
            attack_risk_label = self.attack_risk_classifier.predict([prepared_session_features])[0]
            print(f"Attack risk label: {attack_risk_label}")
            return Label(label=attack_risk_label, uuid=prepared_session.uuid)
        except Exception as e:
            raise Exception(f"An error occurred, cannot classify session: {e}")

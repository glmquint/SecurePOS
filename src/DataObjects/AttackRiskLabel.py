class AttackRiskLabel:
    attackRiskLabel = None
    def __init__(self, attackRiskLabel):
        self.attackRiskLabel = attackRiskLabel

    def getAttackRiskLabel(self):
        return self.attackRiskLabel

    def setAttackRiskLabel(self, attackRiskLabel):
        self.attackRiskLabel = attackRiskLabel
        return self.attackRiskLabel

    def to_json(self):
        return {
            "attackRiskLabel": self.attackRiskLabel,
        }
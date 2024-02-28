class AttackRiskLabel:
    attackRiskLabel = None
    def __init__(self, attackRiskLabel):
        self.attackRiskLabel = attackRiskLabel

    def getAttackRiskLabel(self):
        return self.attackRiskLabel

    def setAttackRiskLabel(self, attackRiskLabel):
        self.attackRiskLabel = attackRiskLabel
        return self.attackRiskLabel

    #define a json schema validator for the class
    def json_schema(self):
        schema = {
            "type": "object",
            "properties": {
                "attackRiskLabel": {
                    "type": "string",
                    "enum": ["low", "medium", "high"]
                }
            },
            "required": ["attackRiskLabel"]
        }
        return schema
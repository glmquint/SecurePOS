class AttackRiskLabel:
    attackRiskLabel = None
    def __init__(self, **kwargs):
        self.attackRiskLabel = kwargs.get("attackRiskLabel", None)

    def to_json(self):
        return self.__dict__

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
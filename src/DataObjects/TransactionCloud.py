class TransactionCloud:
    def __init__(self, UUID, timestamp, amount):
        self.UUID = UUID
        self.timestamp = timestamp
        self.amount = amount

    def to_json(self):
        return {
            "UUID": self.UUID,
            "timestamp": self.timestamp,
            "destIP": self.amount
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            data["UUID"],
            data["timestamp"],
            data["amount"]
        )

    def __str__(self):
        return f"UUID: {self.UUID}, timestamp: {self.timestamp}, amount: {self.amount}"

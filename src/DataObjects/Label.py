class Label:
    def __init__(self, UUID, label):
        self.UUID = UUID
        self.label = label

    def to_json(self):
        return {
            "UUID": self.UUID,
            "label": self.label
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            data["UUID"],
            data["label"]
        )

    def __str__(self):
        return f"UUID: {self.UUID}, label: {self.label}"

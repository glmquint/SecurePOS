class NetworkMonitor:
    def __init__(self, UUID, targetIP, destIP):
        self.UUID = UUID
        self.targetIP = targetIP
        self.destIP = destIP

    def to_json(self):
        return {
            "UUID": self.UUID,
            "targetIP": self.targetIP,
            "destIP": self.destIP
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            data["UUID"],
            data["targetIP"],
            data["destIP"]
        )

    def __str__(self):
        return f"UUID: {self.UUID}, targetIP: {self.targetIP}, destIP: {self.destIP}"

class LocalizationSys:
    def __init__(self, UUID, longitude, latitude):
        self.UUID = UUID
        self.longitude = longitude
        self.latitude = latitude

    def to_json(self):
        return {
            "UUID": self.UUID,
            "longitude": self.longitude,
            "latitude": self.latitude
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            data["UUID"],
            data["longitude"],
            data["latitude"]
        )

    def __str__(self):
        return f"UUID: {self.UUID}, longitude: {self.longitude}, latitude: {self.latitude}"



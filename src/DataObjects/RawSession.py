class RawSession:
    def __init__(self, UUID, LABEL, latitude, longitude, targetIP, destIP, ts, am):
        self.UUID = UUID
        self.LABEL = LABEL
        self.latitude = latitude
        self.longitude = longitude
        self.targetIP = targetIP
        self.destIP = destIP
        self.ts = ts
        self.am = am
    @classmethod
    def from_json(cls, data):
        return cls(
            data["UUID"],
            data["LABEL"],
            data["latitude"],
            data["longitude"],
            data["targetIP"],
            data["destIP"],
            data["ts"],
            data["am"]
        )

    def to_json(self):
        return {
            "UUID": self.UUID,
            "LABEL": self.LABEL,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "targetIP": self.targetIP,
            "destIP": self.destIP,
            "ts": self.ts,
            "am": self.am
        }


if __name__ == "__main__":
    # Example usage:
    json_data = {
        "UUID": "a923-45b7-gh12-2869",
        "LABEL": "normal",
        "latitude": -18.0032216230982,
        "longitude": -84.4669574843863,
        "targetIP": "192.168.25.4",
        "destIP": "192.168.90.203",
        "ts": [7520.38693128729, 7540.01476282207, 7560.84201643904, 7525.55036998267, 7430.31526699634, 7582.75161317361, 7475.14787953081, 7531.53034928949, 7372.96400321726, 7610.16990766799],
        "am": [12.8505469215328, 13.5047152766449, 14.0224623386235, 14.9328568509386, 13.0022587486345, 15.9005029483746, 11.6345719786612, 14.4606348281486, 14.6495303464239, 14.0635376533773]
    }



    network_data = RawSession.from_json(json_data)
    print(network_data.to_json())

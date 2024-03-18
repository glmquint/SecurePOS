import json
from datetime import datetime
from time import sleep


class ElasticitySample:
    def __init__(self, system, event,timestamp):
        self.system = system
        self.event = event
        self.timestamps = timestamp

    def to_json(self):
        return json.dumps({
            "system": self.system,
            "event": self.event,
            "timestamp": self.timestamps.strftime("%Y-%m-%d %H:%M:%S")
        })


if __name__ == "__main__":
    elasticity_sample = ElasticitySample("Production", "Start", datetime.now())
    print(elasticity_sample.to_json())

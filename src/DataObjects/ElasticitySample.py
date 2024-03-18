import json
from datetime import datetime
from time import sleep


class ElasticitySample:
    def __init__(self, number_of_inputs):
        self.number_of_inputs = number_of_inputs
        self.timestamps = {}

    def add_timestamp(self, phase, timestamp):
        self.timestamps[phase] = timestamp

    def serialize_datetime(self):
        if isinstance(self.timestamps, datetime.datetime):
            return self.isoformat()
        raise TypeError("Type not serializable")

    def __str__(self):
        #timestamp_str = ", ".join(f"{phase}: {timestamp}" for phase, timestamp in self.timestamps.items())
        #return f"Number of inputs: {self.number_of_inputs}, Timestamps: {timestamp_str}"
        return

    def to_json(self):
        return json.dumps(self.timestamps,default=self.serialize_datetime)

if __name__ == "__main__":
    elasticity_sample = ElasticitySample(5)
    #print(datetime.now())
    elasticity_sample.add_timestamp("start", datetime.now())
    elasticity_sample.add_timestamp("end", datetime.now())
    print(elasticity_sample.to_json())
    exit()
    c = datetime.now()
    #c = datetime(2022, 12, 28, 23, 55, 59, 342380)
    #c.year()
    print(c.year)
    exit()
    sleep(2)
    #print(elasticity_sample))
    #print(elasticity_sample.to_json())

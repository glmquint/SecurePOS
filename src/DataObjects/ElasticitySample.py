from datetime import datetime
from time import sleep


class ElasticitySample:
    def __init__(self, number_of_inputs):
        self.number_of_inputs = number_of_inputs
        self.timestamps = {}

    def add_timestamp(self, phase, timestamp):
        self.timestamps[phase] = timestamp

    def __str__(self):
        timestamp_str = ", ".join(f"{phase}: {timestamp}" for phase, timestamp in self.timestamps.items())
        return f"Number of inputs: {self.number_of_inputs}, Timestamps: {timestamp_str}"


if __name__ == "__main__":
    elasticity_sample = ElasticitySample(5)
    elasticity_sample.add_timestamp("start", datetime.now())
    sleep(2)
    elasticity_sample.add_timestamp("end", datetime.now())
    print(elasticity_sample)

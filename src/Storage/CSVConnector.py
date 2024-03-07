import csv

class CSVConnector:
    def __init__(self, config):
        self.config = config

    def insert(self, elasticitySample):
        with open(self.config['path'], 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            timestamps = [elasticitySample.timestamps[key] for key in elasticitySample.timestamps]
            writer.writerow([elasticitySample.number_of_inputs] + timestamps)

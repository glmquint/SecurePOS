import csv

class CSVConnector:
    def __init__(self, config):
        self.config = config

    def insert(self, elasticitySample):
        with open(self.config['path'], 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([elasticitySample.system, elasticitySample.event, elasticitySample.timestamps])
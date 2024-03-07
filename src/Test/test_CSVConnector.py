import unittest
from datetime import datetime
from time import sleep

from src.DataObjects.ElasticitySample import ElasticitySample
from src.Storage.CSVConnector import CSVConnector
from src.Storage.StorageController import StorageController


class TestCSVConnector(unittest.TestCase):
    def setUp(self):
        self.config = {'path': 'test.csv'}
        self.connector = CSVConnector(self.config)

    def test_insert(self):
        sample = ElasticitySample(5)
        sample.add_timestamp("start", datetime.now())
        sleep(2)
        sample.add_timestamp("first", datetime.now())
        sleep(1)
        sample.add_timestamp("second", datetime.now())
        sleep(1)
        sample.add_timestamp("end", datetime.now())

        # Insert the sample into the CSV file
        self.connector.insert(sample)

        # Clean up by removing the test CSV file
        import os
        os.remove('test.csv')
    def test_storage(self):
        self.setUp()
        sample = ElasticitySample(5)
        storage_controller = StorageController(self.config, ElasticitySample)
        sample.add_timestamp("start", datetime.now())
        sleep(2)
        sample.add_timestamp("first", datetime.now())
        sleep(1)
        sample.add_timestamp("second", datetime.now())
        sleep(1)
        sample.add_timestamp("end", datetime.now())

        # Insert the sample into the CSV file
        storage_controller.save(sample)

        # Clean up by removing the test CSV file
        #import os
        #os.remove('test.csv')


if __name__ == '__main__':
    unittest.main()


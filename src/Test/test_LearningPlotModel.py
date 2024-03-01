from unittest import TestCase

from src.Development.LearningPlotModel import LearningPlotModel
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig

class TestLearningPlotModel(TestCase):
    dbConfig = DBConfig('training', 'learning_plot', ['loss', 'number_of_generations', 'loss_threshold'])
    lpm = LearningPlotModel(8.4, 100, 0.01)
    lpm2 = LearningPlotModel(0, 0, 0)
    storageController = StorageController(dbConfig, type(lpm))
    def test_populate(self):
        self.storageController.save(self.lpm)
        self.lpm2.populate(self.storageController)
        print(self.lpm2.loss)





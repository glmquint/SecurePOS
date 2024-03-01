from unittest import TestCase

from src.Development.LearningPlotModel import LearningPlotModel
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig

class TestLearningPlotModel(TestCase):
    dbConfig = DBConfig('training', 'learning_plot', ['loss', 'number_of_generations', 'loss_threshold'])
    storageController = StorageController(dbConfig, type(LearningPlotModel))
    def test_populate(self):
        learning_plot_model = LearningPlotModel(self.storageController)







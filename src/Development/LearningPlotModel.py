from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig


class LearningPlotModel:
    loss: float = None
    number_of_generations: int = None
    loss_threshold: float = None

    def populate(self, storage_controller: StorageController):
        list = storage_controller.retrieveAll()
        print(list)
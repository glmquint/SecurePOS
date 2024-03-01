from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig


class LearningPlotModel:
    loss: float = None
    number_of_generations: int = None
    loss_threshold: float = None

    def __init__(self, loss: float, number_of_generations: int, loss_threshold: float):
        self.loss = loss
        self.number_of_generations = number_of_generations
        self.loss_threshold = loss_threshold

    def populate(self, storage_controller: StorageController):
        list = storage_controller.retrieveAll()
        self.loss = list[0][0]
        self.number_of_generations = list[0][1]
        self.loss_threshold = list[0][2]
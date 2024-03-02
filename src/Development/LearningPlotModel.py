from src.Storage.StorageController import StorageController


class LearningPlotModel:
    loss: float = None
    number_of_generations: int = None
    loss_threshold: float = None

    def __init__(self, from_tuple: tuple):
        self.loss, self.number_of_generations, self.loss_threshold = from_tuple


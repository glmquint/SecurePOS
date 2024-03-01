from src.Storage.StorageController import StorageController


class LearningPlotModel:
    loss: float = None
    number_of_generations: int = None
    loss_threshold: float = None

    def __init__(self, storage_controller: StorageController):
        list = storage_controller.retrieve_all()
        self.loss = list[0][0]
        self.number_of_generations = list[0][1]
        self.loss_threshold = list[0][2]
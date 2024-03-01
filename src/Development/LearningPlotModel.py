from src.Storage.StorageController import StorageController


class LearningPlotModel:
    loss: float = None
    number_of_generations: int = None
    loss_threshold: float = None

    def populate(self, st: StorageController):
        list = st.retrieveAll()

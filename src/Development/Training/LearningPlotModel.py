
class LearningPlotModel:
    loss: [float] = None
    number_of_generations: int = None
    loss_threshold: float = None

    def __init__(self, from_tuple: tuple):
        self.loss, self.number_of_generations, self.loss_threshold = from_tuple

    ([0.01,2e34,0.1],100,0.1)
    0.01,100,0.1
    2e43,100,0.1

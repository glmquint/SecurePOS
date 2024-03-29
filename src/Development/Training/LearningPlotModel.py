class LearningPlotModel:
    loss_curve = None
    number_of_generations: int = None
    loss_threshold: float = None

    def __init__(
            self,
            loss_curve: list,
            number_of_generations: int,
            loss_threshold: float):
        self.loss_curve = loss_curve
        self.number_of_generations = number_of_generations
        self.loss_threshold = loss_threshold

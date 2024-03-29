class LearningPlotModel:
    """
    A class used to model the learning plot in the development system.

    Attributes
    ----------
    loss_curve : list
        The curve representing the loss during the learning process.
    number_of_generations : int
        The number of generations in the learning process.
    loss_threshold : float
        The threshold for the loss in the learning process.

    Methods
    -------
    __init__(self, loss_curve: list, number_of_generations: int, loss_threshold: float)
        Initializes the LearningPlotModel class with a loss curve, number of generations, and a loss threshold.
    """
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

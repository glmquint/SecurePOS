from src.Development.Training.LearningPlotModel import LearningPlotModel
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('Agg')


class LearningPlotView:
    """
    A class used to view the learning plot in the development system.

    Attributes
    ----------
    path_to_save : str
        The path where the learning plot will be saved.
    model : LearningPlotModel
        The model of the learning plot.

    Methods
    -------
    __init__(self, filename: str, learning_plot_model: LearningPlotModel)
        Initializes the LearningPlotView class with a filename and a learning plot model.
    update(self)
        Updates the learning plot view by saving the model to a PNG file.
    """
    # class implementation...class LearningPlotView:
    path_to_save: str = None
    model: LearningPlotModel = None

    def __init__(self, filename: str, learning_plot_model: LearningPlotModel):
        self.path_to_save = f'{os.path.dirname(__file__)}/{filename}.png'
        self.model = learning_plot_model

    def update(self):
        if os.path.exists(self.path_to_save):
            os.remove(self.path_to_save)
        plt.plot(
            range(
                1,
                self.model.number_of_generations),
            self.model.loss_curve,
            label='Loss')
        plt.xticks(range(1, self.model.number_of_generations))
        plt.xlabel('Number of generations')
        plt.ylabel('Loss')
        plt.title(
            f'Learning plot (Loss threshold: {self.model.loss_threshold})')
        plt.savefig(self.path_to_save)
        plt.close()

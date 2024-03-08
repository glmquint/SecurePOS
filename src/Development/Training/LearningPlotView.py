import matplotlib.pyplot as plt

from src.Development.Training.LearningPlotModel import LearningPlotModel


class LearningPlotView:
    path_to_save: str = None
    model: LearningPlotModel = None

    def __init__(self, filename: str, learning_plot_model: LearningPlotModel):
        self.path_to_save = f'src/Development/{filename}.png'
        self.model = learning_plot_model

    def update(self):
        plt.plot(range(1, self.model.number_of_generations + 1), self.model.loss_curve, label='Loss')
        plt.xlabel('Number of generations')
        plt.ylabel('Loss')
        plt.savefig(self.path_to_save)

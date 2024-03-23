import os

import matplotlib.pyplot as plt

from src.Development.Training.LearningPlotModel import LearningPlotModel


class LearningPlotView:
    path_to_save: str = None
    model: LearningPlotModel = None

    def __init__(self, filename: str, learning_plot_model: LearningPlotModel):
        self.path_to_save = f'{os.path.dirname(__file__)}/Training/{filename}.png'
        self.model = learning_plot_model

    def update(self):
        if os.path.exists(self.path_to_save):
            os.remove(self.path_to_save)
        plt.plot(range(1, self.model.number_of_generations), self.model.loss_curve, label='Loss')
        plt.xticks(range(1, self.model.number_of_generations))
        plt.xlabel('Number of generations')
        plt.ylabel('Loss')
        plt.title(f'Learning plot (Loss threshold: {self.model.loss_threshold})')
        plt.savefig(self.path_to_save)
        plt.close()

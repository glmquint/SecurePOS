import matplotlib.pyplot as plt

from src.Development.LearningPlotModel import LearningPlotModel


class LearningPlotView:
    path_to_save: str = None
    model: LearningPlotModel = None

    def __init__(self, filename: str, learning_plot_model: LearningPlotModel):
        self.path_to_save = f'src/Development/{filename}.png'
        self.model = learning_plot_model

    def update(self):
        # TODO: implement the figure update using the model
        plt.xlabel('Number of generations')
        plt.ylabel('Loss')
        plt.savefig("data/learning_plot.png")

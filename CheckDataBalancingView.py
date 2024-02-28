import matplotlib.pyplot as plt
import numpy as np
import PreparedSession


class CheckDataBalance:
    toleraceParameter = 0

    def __init__(self, toleraceParameter):
        self.toleraceParameter = toleraceParameter

    def plotCheckDataBalance(self, PreparedSessionList):

        labels = ['Low', 'Medium', 'High']

        values = [0, 0, 0]

        for i in PreparedSessionList:
            match i.label:
                case "Low":
                    values[0] += 1
                case "Medium":
                    values[1] += 1
                case "High":
                    values[2] += 1
                case _:
                    continue

        # Set the width of the bars
        bar_width = 0.6

        # Set the positions of the bars on the x-axis
        bar_positions1 = np.arange(len(labels))
        bar_positions2 = [pos + bar_width for pos in bar_positions1]

        yer1 = [0.5, 0.4, 0.5]
        average = (values[0] + values[1] + values[2]) / 3

        plt.bar(bar_positions2, values, width=bar_width, yerr=average * self.toleraceParameter / 100)

        plt.axhline(y=average, linewidth=1, color='k')

        # Add title and labels
        plt.title('Data Balance')
        plt.xlabel('Labels')
        plt.ylabel('Values')

        # Set x-axis tick positions and labels
        plt.xticks([pos + bar_width for pos in bar_positions1], labels)

        plt.show()


def test():
    c = CheckDataBalance(5)
    p1 = []
    for i in range(0, 20):
        p1.append(PreparedSession(0, 0, 0, 0, 0, 0, "High"))

    p2 = []
    for i in range(0, 15):
        p2.append(PreparedSession(0, 0, 0, 0, 0, 0, "Medium"))

    p3 = []
    for i in range(0, 18):
        p3.append(PreparedSession(0, 0, 0, 0, 0, 0, "Low"))

    c.plotCheckDataBalance(p1 + p2 + p3)

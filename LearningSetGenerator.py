from PreparedSession import *


class LearningSetGenerator:
    trainPercentage = 0
    testPercentage = 0
    validationPercentage = 0

    def __init__(self, trainPercentage, testPercentage, validationPercentage):
        self.trainPercentage = trainPercentage
        self.testPercentage = testPercentage
        self.validationPercentage = validationPercentage

    def generateLearningSet(self, PreparedSessionList):
        # to be implemented
        return ["ciao"]


def test():
    l = LearningSetGenerator(70, 15, 15)
    p1 = []
    for i in range(0, 20):
        p1.append(PreparedSession(0, 0, 0, 0, 0, 0, "High"))

    p2 = []
    for i in range(0, 15):
        p2.append(PreparedSession(0, 0, 0, 0, 0, 0, "Medium"))

    p3 = []
    for i in range(0, 18):
        p3.append(PreparedSession(0, 0, 0, 0, 0, 0, "Low"))

    l.generateLearningSet(p1 + p2 + p3)

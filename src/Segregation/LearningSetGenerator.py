from PreparedSession import *
from src.Segregation.LearningSet import LearningSet


class LearningSetGenerator:

    def __init__(self, trainPercentage, testPercentage, validationPercentage, storageController):
        self.__trainPercentage = trainPercentage
        self.__testPercentage = testPercentage
        self.__validationPercentage = validationPercentage
        self.__storageController = storageController

    def generateLearningSet(self):
        preparedSessionArray = self.__storageController.retrieveAll()
        cardinalityPreparedSession = self.__storageController.countAll()

        testSetCardinality = int(cardinalityPreparedSession*self.__testPercentage)
        valSetCardinality = int(cardinalityPreparedSession*self.__validationPercentage)
        trainingSetCardinality = cardinalityPreparedSession - testSetCardinality-valSetCardinality

        learningSet = LearningSet(
                        preparedSessionArray[:trainingSetCardinality],
                        preparedSessionArray[trainingSetCardinality:trainingSetCardinality+testSetCardinality],
                        preparedSessionArray[trainingSetCardinality+testSetCardinality:]
                    )
        return learningSet


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

import pandas as pd
from src.DataObjects.LearningSet import LearningSet
import math


class LearningSetGenerator:

    def __init__(self, trainPercentage, testPercentage, validationPercentage, storageController):
        self.__trainPercentage = trainPercentage
        self.__testPercentage = testPercentage
        self.__validationPercentage = validationPercentage
        self.__storageController = storageController
        self.leaning_set = None

    def generate_learning_set(self):
        preparedSessionArray = self.__storageController.retrieve_all(False)
        cardinalityPreparedSession = self.__storageController.count(False)

        testSetCardinality = math.ceil(cardinalityPreparedSession * self.__testPercentage / 100)
        valSetCardinality = math.ceil(cardinalityPreparedSession * self.__validationPercentage / 100)
        trainingSetCardinality = cardinalityPreparedSession - testSetCardinality - valSetCardinality

        trainingSet = preparedSessionArray[:trainingSetCardinality]
        validationSet = preparedSessionArray[trainingSetCardinality:trainingSetCardinality + testSetCardinality]
        testSet = preparedSessionArray[trainingSetCardinality + testSetCardinality:]

        trainingSetArray = validationSetArray = testSetArray = []
        trainingSetLabel = validationSetLabel = testSetLabel = []

        for i in trainingSet:
            trainingSetArray.append(i.returnArray())
            trainingSetLabel.append((i.getLabel()))

        for i in validationSet:
            validationSetArray.append(i.returnArray())
            validationSetLabel.append((i.getLabel()))

        for i in testSet:
            testSetArray.append(i.returnArray())
            testSetLabel.append((i.getLabel()))

        trainingSetArray = pd.DataFrame(trainingSetArray).drop([6], axis=1)
        validationSetArray = pd.DataFrame(validationSetArray).drop([6], axis=1)
        testSetArray = pd.DataFrame(testSetArray).drop([6], axis=1)

        dic = dict()
        dic['trainingSet'] = trainingSetArray
        dic['validationSet'] = validationSetArray
        dic['testSet'] = testSetArray
        dic['trainingSetLabel'] = trainingSetLabel
        dic['validationSetLabel'] = validationSetLabel
        dic['testSetLabel'] = testSetLabel

        learningSet = LearningSet(dic, False)
        self.leaning_set = learningSet

import pandas as pd
from src.Segregation.LearningSet import LearningSet
import math


class LearningSetGenerator:

    def __init__(self, trainPercentage, testPercentage, validationPercentage, storageController, messageBus):
        self.__trainPercentage = trainPercentage
        self.__testPercentage = testPercentage
        self.__validationPercentage = validationPercentage
        self.__storageController = storageController
        self.__messageBus = messageBus

    def generateLearningSet(self):
        preparedSessionArray = self.__storageController.retrieveAll()
        cardinalityPreparedSession = self.__storageController.countAll()

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

        trainingSetArray = pd.DataFrame(trainingSetArray).drop([0, 7], axis=1)
        validationSetArray = pd.DataFrame(validationSetArray).drop([0, 7], axis=1)
        testSetArray = pd.DataFrame(testSetArray).drop([0, 7], axis=1)

        dic = dict()
        dic['trainingSet'] = trainingSetArray
        dic['validationSet'] = validationSetArray
        dic['testSet'] = testSetArray
        dic['trainingSetLabel'] = trainingSetLabel
        dic['validationSetLabel'] = validationSetLabel
        dic['testSetLabel'] = testSetLabel

        learningSet = LearningSet(dic, False)
        self.__messageBus.pushTopic("leaningSet", learningSet)

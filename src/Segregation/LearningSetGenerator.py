from PreparedSession import *
from src.Segregation.LearningSet import LearningSet
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig
import math
import json

class LearningSetGenerator:

    def __init__(self, trainPercentage, testPercentage, validationPercentage, storageController):
        self.__trainPercentage = trainPercentage
        self.__testPercentage = testPercentage
        self.__validationPercentage = validationPercentage
        self.__storageController = storageController

    def generateLearningSet(self):
        preparedSessionArray = self.__storageController.retrieveAll()
        cardinalityPreparedSession = self.__storageController.countAll()

        testSetCardinality = math.ceil(cardinalityPreparedSession*self.__testPercentage/100)
        valSetCardinality = math.ceil(cardinalityPreparedSession*self.__validationPercentage/100)
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
        p1.append(PreparedSession([0, 0, 0, 0, 0, 0, "High"]))

    p2 = []
    for i in range(0, 15):
        p2.append(PreparedSession([0, 0, 0, 0, 0, 0, "Medium"]))

    p3 = []
    for i in range(0, 18):
        p3.append(PreparedSession([0, 0, 0, 0, 0, 0, "Low"]))

    l.generateLearningSet(p1 + p2 + p3)

def test1():
    dbConfig = DBConfig("PreparedSessionsDataStore", "PreparedSessions")
    # ['MeanAbsoluteDifferencingTransactionTimestamps', 'MeanAbsoluteDifferencingTransactionAmount','MedianLongitude', 'MedianLatitude', 'MedianTargetIP', 'MedianDestIP', 'Label']
    storageController = StorageController(dbConfig, PreparedSession)
    l = LearningSetGenerator(70, 15, 15,storageController)
    l.generateLearningSet()
test1()
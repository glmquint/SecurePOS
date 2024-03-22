import pandas as pd
from src.DataObjects.LearningSet import LearningSet
import math

from src.DataObjects.Session import PreparedSession


class LearningSetGenerator:

    def __init__(self, trainPercentage, testPercentage, validationPercentage, storageController):
        self.__trainPercentage = trainPercentage
        self.__testPercentage = testPercentage
        self.__validationPercentage = validationPercentage
        self.__storageController = storageController
        self.leaning_set = None

    def generate_learning_set(self):
        preparedSessionArray : [PreparedSession] = self.__storageController.retrieve_all(False)
        cardinalityPreparedSession = self.__storageController.count(False)
        assert len(preparedSessionArray) == cardinalityPreparedSession, f"got unexpected cardinality for prepared session: {cardinalityPreparedSession} instead of {len(preparedSessionArray)}"

        # calculate train, test and validation splits
        testSetCardinality = math.ceil(cardinalityPreparedSession * self.__testPercentage)
        valSetCardinality = math.ceil(cardinalityPreparedSession * self.__validationPercentage)
        trainingSetCardinality = cardinalityPreparedSession - testSetCardinality - valSetCardinality

        # split the dataset into train, test and validation
        trainingSet = preparedSessionArray[:trainingSetCardinality]
        validationSet = preparedSessionArray[trainingSetCardinality:trainingSetCardinality + testSetCardinality]
        testSet = preparedSessionArray[trainingSetCardinality + testSetCardinality:]

        # prepare the dictionaries to be converted into dataframes
        cols = trainingSet[0].to_json().keys() - {'uuid'}
        trainingSetArray = dict(zip(cols, [0] * len(cols)))
        validationSetArray = dict(zip(cols, [0] * len(cols)))
        testSetArray = dict(zip(cols, [0] * len(cols)))
        for col in cols:
            trainingSetArray[col]   = [v.to_json()[col] for v in trainingSet]
            validationSetArray[col] = [v.to_json()[col] for v in validationSet]
            testSetArray[col]       = [v.to_json()[col] for v in testSet]

        # target labels are stored on a separate array
        trainingSetLabel = trainingSetArray.pop('label')
        validationSetLabel = validationSetArray.pop('label')
        testSetLabel = testSetArray.pop('label')

        # convert into named dataframes
        trainingSetArray = pd.DataFrame(trainingSetArray)
        validationSetArray = pd.DataFrame(validationSetArray)
        testSetArray = pd.DataFrame(testSetArray)

        dic = dict()
        dic['trainingSet'] = trainingSetArray
        dic['validationSet'] = validationSetArray
        dic['testSet'] = testSetArray
        dic['trainingSetLabel'] = trainingSetLabel
        dic['validationSetLabel'] = validationSetLabel
        dic['testSetLabel'] = testSetLabel

        learningSet = LearningSet(dic, False)

        ''' TODO: after cleaning the constructor, this will be possible
        learningSet = LearningSet(
            trainingSetArray = trainingSetArray,
            validationSetArray = validationSetArray,
            testSetArray = testSetArray,
            trainingSetLabel = trainingSetLabel,
            validationSetLabel = validationSetLabel,
            testSetLabel = testSetLabel
        )
        '''

        self.leaning_set = learningSet

import pandas as pd

class LearningSet:
    trainingSet = None
    validationSet = None
    testSet = None
    trainingSetLabel = None
    validationSetLabel = None
    testSetLabel = None

    def __init__(self, dic, fromJson: False):
        if fromJson:
            self.learningSetfromJson(dic)
            return
        self.trainingSet = dic['trainingSet']
        self.validationSet = dic['validationSet']
        self.testSet = dic['testSet']
        self.trainingSetLabel = dic['trainingSetLabel']
        self.validationSetLabel = dic['validationSetLabel']
        self.testSetLabel = dic['testSetLabel']

    def learningSetfromJson(self, dic):
        self.trainingSet =  pd.DataFrame(dic['trainingSet']['data'], columns=dic['trainingSet']['columns'])
        self.validationSet = pd.DataFrame(dic['validationSet']['data'], columns=dic['validationSet'] ['columns'])
        self.testSet =  pd.DataFrame(dic['testSet']['data'], columns=dic['testSet']['columns'])
        self.trainingSetLabel = dic['trainingSetLabel']
        self.validationSetLabel = dic['validationSetLabel']
        self.testSetLabel = dic['testSetLabel']

    def toJson(self):
        data = {
                'trainingSet': self.trainingSet.to_dict(orient="split"),
                'validationSet': self.validationSet.to_dict(orient="split"),
                'testSet': self.testSet.to_dict(orient="split"),
                'trainingSetLabel': self.trainingSetLabel,
                'validationSetLabel': self.validationSetLabel,
                'testSetLabel': self.testSetLabel
        }
        return data

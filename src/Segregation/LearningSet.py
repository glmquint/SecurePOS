import json


class LearningSet:
    trainingSet = []
    validationSet = []
    testSet = []
    trainingSetLabel = []
    validationSetLabel = []
    testSetLabel = []

    def __init__(self, trainingSet, validationSet, testSet,trainingSetLabel,validationSetLabel,testSetLabel):
        self.trainingSet = trainingSet
        self.validationSet = validationSet
        self.testSet = testSet
        self.trainingSetLabel = trainingSetLabel
        self.validationSetLabel = validationSetLabel
        self.testSetLabel = testSetLabel

    def to_json(self):
        dic = dict()
        dic["trainingSet"] = self.trainingSet.to_json()
        dic["validationSet"] = self.validationSet.to_json()
        dic["testSet"] = self.testSet.to_json()
        dic["trainingSetLabel"] = self.trainingSetLabel
        dic["validationSetLabel"] = self.validationSetLabel
        dic["testSetLabel"] = self.testSetLabel

        ciao = ("{"
                "trainingSet : "+self.trainingSet.to_json()
                +",validationSet:"+self.validationSet.to_json()
                +",testSet:"+self.testSet.to_json()+",trainingSetLabel"
                +",trainingSetLabel: "+json.dumps(self.trainingSetLabel)
                + ",validationSetLabel: " + json.dumps(self.trainingSetLabel)
                + ",trainingSetLabel: " + json.dumps(self.trainingSetLabel)
                )


        return




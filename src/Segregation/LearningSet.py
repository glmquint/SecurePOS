import json


class LearningSet:
    __trainingSet = []
    __validationSet = []
    __testSet = []

    def __init__(self, trainingSet, validationSet, testSet):
        for p in trainingSet:
            l = [p, p.label]
            self.__trainingSet.append(l)

        for p in validationSet:
            l = [p, p.label]
            self.__validationSet.append(l)

        for p in testSet:
            l = [p, p.label]
            self.__testSet.append(l)

    def toJSON(self):
        #TODO i label conviene metterli fuori dalla prepared session?
        trainingSet = "["
        for p in self.__trainingSet:
            trainingSet += "{"
            trainingSet += str(p[0].__dict__)
            trainingSet += ", label: "+p[1]+"},"

        ciao = 0
        pass


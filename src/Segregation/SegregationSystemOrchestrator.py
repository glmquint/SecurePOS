from LearningSetGenerator import *
from random import random
import numpy as np

from SegregationPlotController import SegregationPlotController
from src.Segregation.SegregationSystemConfig import SegregationSystemConfig
from src.Storage.StorageController import StorageController

from src.Storage.dbConfig import DBConfig


def send(data):
    # send data
    return 0

def recive():
    # recive
    label = ["High", "Medium", "Low"]
    test_array = np.array(label)
    random_num = np.random.choice(test_array)
    params = [random(), random(), random(), random(), random(), random(), random_num]
    p = PreparedSession(params)
    return p

def run():
    # get config parameter
    configParameter = SegregationSystemConfig()
    serviceFlag = configParameter.getServiceFlag()
    limitPreparedSession = configParameter.getSufficientSessionNumber()

    dbConfig = DBConfig("PreparedSessionsDataStore", "PreparedSessions")
    # ['MeanAbsoluteDifferencingTransactionTimestamps', 'MeanAbsoluteDifferencingTransactionAmount','MedianLongitude', 'MedianLatitude', 'MedianTargetIP', 'MedianDestIP', 'Label']
    storageController = StorageController(dbConfig, PreparedSession)
    segregationPlotController = SegregationPlotController(storageController,
                                                          configParameter.getToleranceDataBalancing())


    # storageController.createTable()

    while True:
        evaluationCheckDataBalance = ""
        evaluationCheckInputCoverage = ""
        if serviceFlag is False:
            # the serviceFlag is false if the simplified stop and go interaction is not active
            evaluationCheckDataBalance = segregationPlotController.getCheckDataBalance()
            evaluationCheckInputCoverage = segregationPlotController.getCheckInputCoverage()
            if evaluationCheckInputCoverage == "no":
                # if the coverage is not satisfied the process has to start from the start
                segregationPlotController.setEvaluationCheckDataBalance("checking")
                segregationPlotController.setEvaluationCheckInputCoverage("checking")
                evaluationCheckDataBalance = "checking"
                evaluationCheckInputCoverage = "checking"

        if serviceFlag is True or evaluationCheckDataBalance != "ok":
            # loop until I receive enough prepared session

            while (storageController.countAll()) != limitPreparedSession:
                # TODO implementare il reciver
                p = recive()
                storageController.save(p)
                print(storageController.countAll())

            # plot the graph
            segregationPlotController.plotDataBalance()

            if serviceFlag is False:
                break
            else:  # simulate the decision of the human
                evaluationDataBalanceCheck = segregationPlotController.getSimulatedCheckDataBalance()
                if evaluationDataBalanceCheck == "no":  # the test will not pass with a probability of 90%
                    # "data not balanced"
                    continue

        if serviceFlag is True or (evaluationCheckDataBalance == "ok" and evaluationCheckInputCoverage != "ok"):
            # here the human have checked that the data are correctly balanced

            # plot the checkInputCoverage graph
            segregationPlotController.plotCheckInputCoverage()

            # let's check input coverage
            if serviceFlag is False:
                break
            else:
                evaluationCheckinputCoverage = segregationPlotController.getSimulatedCheckInputCoverage()
                # "input not covered"
                if evaluationCheckinputCoverage <= 0.1:
                    continue

        if serviceFlag is True or (evaluationCheckDataBalance == "ok" and evaluationCheckInputCoverage == "ok"):
            # normalize data
            storageController.normalizeData()

            # here the human have checked that the data are correctly balanced
            learningSetGenerator = LearningSetGenerator(configParameter.getPercentageTrainingSplit(),
                                                        configParameter.getPercentageTestSplit(),
                                                        configParameter.getPercentageValidationSplit(),
                                                        storageController)
            # generate learning set
            learningSet = learningSetGenerator.generateLearningSet()

            send(learningSet)
            storageController.removeAll()  # remove the session

            # reset the evaluation in report files
            segregationPlotController.setEvaluationCheckDataBalance("checking")
            segregationPlotController.setEvaluationCheckInputCoverage("checking")


if __name__ == "__main__":
    run()

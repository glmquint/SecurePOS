from LearningSetGenerator import *
from random import random
import numpy as np

from SegregationPlotController import *
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

        if serviceFlag is False:
            # if the simplified stop and go interaction is not active
            with open('Data/checkDataBalanceReport.json', 'r') as checkDataBalanceFile:
                jsonData = json.load(checkDataBalanceFile)
                evaluationCheckDataBalance = jsonData.get("evaluation")
                checkDataBalanceFile.close()

            with open('Data/checkInputCoverageReport.json', 'r') as checkInputCoverageFile:
                jsonData = json.load(checkInputCoverageFile)
                evaluationCheckInputCoverage = jsonData.get("evaluation")
                checkInputCoverageFile.close()

        if serviceFlag is True or evaluationCheckDataBalance == "no":
            # loop until I receive enough prepared session
            while (storageController.countAll()) != limitPreparedSession:
                # TODO implementare il reciver
                p = recive()
                storageController.save(p)
                print(storageController.countAll())

            if serviceFlag is True:
                # result obtained stochastically
                evaluationDataBalanceCheck = random()
                if evaluationDataBalanceCheck <= 0.5:
                    # sendToMessagingSystem("data not balanced")
                    # wait until new preparedSession are received
                    # TODO upgrade the limitSession
                    continue
            else:
                segregationPlotController.plotDataBalance()
                # The application ends | the user insert the result in a json | then he reopens the application
                break

        if serviceFlag is True or (evaluationCheckDataBalance == "ok" and evaluationCheckInputCoverage == "no"):
            # here the human have checked that the data are correctly balanced

            # let's check input coverage
            if serviceFlag:
                # result obtained stochastically
                evaluationCheckinputCoverage = random()
                if evaluationCheckinputCoverage <= 0.5:
                    #sendToMessagingSystem("input not covered")
                    # wait until new preparedSession are received
                    # TODO upgrade the limitSession
                    continue
            else:
                segregationPlotController.plotCheckInputCoverage()
                # the application ends and the user write the evaluaiton into a json file
                break

        if serviceFlag is True or (evaluationCheckDataBalance == "ok" and evaluationCheckInputCoverage == "ok"):
            # here the human have checked that the data are correctly balanced
            learningSetGenerator = LearningSetGenerator(configParameter.getPercentageTrainingSplit(),
                                                        configParameter.getPercentageTestSplit(),
                                                        configParameter.getPercentageValidationSplit(),
                                                        storageController)
            # generate learning set
            learninSet = learningSetGenerator.generateLearningSet()

            send(learninSet)
            # FIXME quando rimuovere le prepared session?
            storageController.removeAll()

            # reset the evaluation in report files
            with open('Data/checkDataBalanceReport.json', 'w') as f:
                json.dump({"evaluation": "no"}, f)
                f.close()

            with open('Data/checkInputCoverageReport.json', 'w') as f:
                json.dump({"evaluation": "no"}, f)
                f.close()


if __name__ == "__main__":
    run()

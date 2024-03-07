from threading import Thread

from LearningSetGenerator import *
from random import random
import numpy as np

from SegregationPlotController import SegregationPlotController
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Segregation.SegregationSystemConfig import SegregationSystemConfig
from src.Storage.StorageController import StorageController

from src.Storage.dbConfig import DBConfig


def send(data): # FIXME just for debug
    # send data
    return 0


def recive(): # FIXME just for debug
    # recive
    label = ["High", "Medium", "Low"]
    test_array = np.array(label)
    random_num = np.random.choice(test_array)
    d = {'MeanAbsoluteDifferencingTransactionTimestamps': random(),
         'MeanAbsoluteDifferencingTransactionAmount': random(),
         'MedianLongitude': random(),
         'MedianLatitude': random(),
         'MedianTargetIP': random(),
         'MedianDestIP': random(),
         'Label': random_num
         }

    # d = [random(), random(), random(), random(), random(), random(), random_num]

    p = PreparedSession(d)
    return p


def run():
    # get config parameter
    configParameter = SegregationSystemConfig()
    serviceFlag = configParameter.getServiceFlag()
    limitPreparedSession = configParameter.getSufficientSessionNumber()

    messageBus = MessageBus(["preparedSession"])

    dbConfig = DBConfig("PreparedSessionsDataStore", "PreparedSessions")
    # ['MeanAbsoluteDifferencingTransactionTimestamps', 'MeanAbsoluteDifferencingTransactionAmount','MedianLongitude', 'MedianLatitude', 'MedianTargetIP', 'MedianDestIP', 'Label']
    storageController = StorageController(dbConfig, PreparedSession, messageBus)
    segregationPlotController = SegregationPlotController(storageController,
                                                          configParameter.getToleranceDataBalancing())

    # storageController.createTable()

    while True:
        server = 1
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

            if server == 1:
                server = Server()
                test_callback = lambda json_data: messageBus.pushTopic("preparedSession", PreparedSession(json_data))
                server.add_resource(JSONEndpoint, "/segregationSystem", recv_callback=test_callback,
                                    json_schema_path="../DataObjects/Schema/PreparedSessionSchema.json")
                # server.add_resource(JSONEndpoint, "/segregationSystem", recv_callback=test_callback)
                thread = Thread(target=server.run)
                thread.daemon = True  # this will allow the main thread to exit even if the server is still running
                thread.start()

            while (storageController.countAll()) <= limitPreparedSession:
                if server == 0:  # FIXME da elimnare: solo per debug
                    p = recive()
                    storageController.messageBus.pushTopic("preparedSession", p)
                    storageController.save()
                else:
                    # the storage controller will retrive the data from the message bus and will store into the db
                    storageController.save()

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
                if evaluationCheckinputCoverage == "no":
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

            if server == 1:
                # TODO implement learningSet to json
                developmentSystemIp = configParameter.getDevelopmentSystemIp()
                developmentSystemPort = configParameter.getDevelopmentSystemPort()
                developmentSystemEndpoint = configParameter.getDevelopmentSystemEndpoint()
                sender = JSONSender("../DataObjects/Schema/LearningSetSchema.json",
                                    "http://" + str(developmentSystemIp) + ":" + str(
                                        developmentSystemPort) + "/"+str(developmentSystemEndpoint))
                sender.send(learningSet)
            else:
                send(learningSet)

            storageController.removeAll()  # remove the session

            # reset the evaluation in report files
            segregationPlotController.setEvaluationCheckDataBalance("checking")
            segregationPlotController.setEvaluationCheckInputCoverage("checking")


if __name__ == "__main__":
    run()

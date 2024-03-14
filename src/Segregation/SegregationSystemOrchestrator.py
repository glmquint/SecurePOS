from LearningSetGenerator import *
from SegregationPlotController import SegregationPlotController
from src.MessageBus.MessageBus import MessageBus
from src.Segregation.SegregationSystemReceiver import PreparedSessionReceiver
from src.Segregation.SegregationSystemConfig import SegregationSystemConfig
from src.Segregation.SegregationSystemSender import SegregationSystemSender
from src.Storage.StorageController import StorageController
from src.Segregation.PreparedSession import PreparedSession
from src.Storage.dbConfig import DBConfig


def run():
    # get config parameter
    configParameter = SegregationSystemConfig()
    serviceFlag = configParameter.getServiceFlag()
    limitPreparedSession = configParameter.getSufficientSessionNumber()
    segregationSystemPort = configParameter.getSegregationSystemPort()

    # declare message bus
    messageBus = MessageBus(["preparedSession", "leaningSet"])

    # istantiate database
    dbConfig = DBConfig("PreparedSessionsDataStore", "PreparedSessions")
    storageController = StorageController(dbConfig, PreparedSession, messageBus)
    segregationPlotController = SegregationPlotController(storageController,
                                                          configParameter.getToleranceDataBalancing())
    # instantiate and run receiver
    preparedSessionReceiver = PreparedSessionReceiver(messageBus, segregationSystemPort)
    # the server starts to run
    preparedSessionReceiver.run()
    while True:

        evaluationCheckDataBalance = ""
        evaluationCheckInputCoverage = ""
        print("Server started")  # the serviceFlag is false if the simplified stop and go interaction is not active

        if serviceFlag is False:
            evaluationCheckDataBalance = segregationPlotController.getCheckDataBalance()
            evaluationCheckInputCoverage = segregationPlotController.getCheckInputCoverage()
            if evaluationCheckInputCoverage == "not performed":
                # if the coverage is not satisfied the process has to start from the start
                segregationPlotController.setEvaluationCheckDataBalance("checking")
                segregationPlotController.setEvaluationCheckInputCoverage("checking")
                evaluationCheckDataBalance = "checking"
                evaluationCheckInputCoverage = "checking"

        if serviceFlag is True or evaluationCheckDataBalance != "ok":
            # loop until I receive enough prepared session

            print("Receiving data...")
            while (storageController.countAll()) < limitPreparedSession:
                # the storage controller will retrive the data from the messageBus and will store into the db
                storageController.save()

            print("Data correctly stored")

            # plot the graph
            segregationPlotController.plotDataBalance()
            print("Check data balance correctly plotted")

            if serviceFlag is False:
                break
            else:  # simulate the decision of the human
                evaluationDataBalanceCheck = segregationPlotController.getSimulatedCheckDataBalance()
                if evaluationDataBalanceCheck == "not performed":  # the test will not pass with a probability of 90%
                    # "data not balanced"
                    continue

        if serviceFlag is True or (evaluationCheckDataBalance == "ok" and evaluationCheckInputCoverage != "ok"):
            # here the human have checked that the data are correctly balanced

            # plot the checkInputCoverage graph
            segregationPlotController.plotCheckInputCoverage()
            print("Check input coverage correctly plotted")

            # let's check input coverage
            if serviceFlag is False:
                break
            else:
                evaluationCheckinputCoverage = segregationPlotController.getSimulatedCheckInputCoverage()
                # "input not covered"
                if evaluationCheckinputCoverage == "not performed":
                    continue

        if serviceFlag is True or (evaluationCheckDataBalance == "ok" and evaluationCheckInputCoverage == "ok"):
            # TODO i have to normalize data?
            # storageController.normalizeData()

            # here the human have checked that the data are correctly balanced
            # generate the learningSet
            learningSetGenerator = LearningSetGenerator(configParameter.getPercentageTrainingSplit(),
                                                        configParameter.getPercentageTestSplit(),
                                                        configParameter.getPercentageValidationSplit(),
                                                        storageController, messageBus)
            learningSetGenerator.generateLearningSet()
            print("Learning set generated")

            # TODO if the sending returned error i have to reperform the sending

            sender = SegregationSystemSender(messageBus)
            # sender.sendToDevelopment()

            # storageController.removeAll()  # remove the sessions

            # reset the evaluation in report files
            segregationPlotController.setEvaluationCheckDataBalance("checking")
            segregationPlotController.setEvaluationCheckInputCoverage("checking")

            x = input('Do you want to continue: [Yes|No]')
            if "No" in x:
                break


if __name__ == "__main__":
    run()

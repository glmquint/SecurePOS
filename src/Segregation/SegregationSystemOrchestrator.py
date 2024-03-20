from LearningSetGenerator import *
from SegregationPlotController import SegregationPlotController
from src.MessageBus.MessageBus import MessageBus
from src.Segregation.SegregationSystemReceiver import PreparedSessionReceiver
from src.Segregation.SegregationSystemConfig import SegregationSystemConfig
from src.Segregation.SegregationSystemSender import SegregationSystemSender
from src.Storage.StorageController import StorageController
from src.DataObjects.PreparedSession import PreparedSession
from src.Storage.dbConfig import DBConfig


# def createTable(self):  # FIXME for debug
#    return self.DBConnector.createTable()


def run():
    # get config parameter
    configParameter = SegregationSystemConfig()
    serviceFlag = configParameter.getServiceFlag()
    limitPreparedSession = configParameter.getSufficientSessionNumber()
    segregationSystemPort = configParameter.getSegregationSystemPort()

    # declare message bus
    messageBus = MessageBus(["leaningSet"])

    # instantiate database
    # dbConfig = DBConfig("PreparedSessionsDataStore", "PreparedSessions")
    storageController = StorageController({'name': 'PreparedSessionsDataStore', 'table_name': 'PreparedSessions'},
                                          PreparedSession)
    segregationPlotController = SegregationPlotController(storageController,
                                                          configParameter.getToleranceDataBalancing())
    # instantiate and run receiver
    preparedSessionReceiver = PreparedSessionReceiver(messageBus, storageController)
    # the server starts to run
    # storageController.createTable()
    preparedSessionReceiver.run()

    # storageController.removeAll()

    while True:

        evaluationCheckDataBalance = ""
        evaluationCheckInputCoverage = ""
        print("Server started")  # the serviceFlag is false if the simplified stop and go interaction is not active

        if serviceFlag is False:
            # the value that can be assigned to the following two variable is ( checking | ok | not balanced )
            evaluationCheckDataBalance = segregationPlotController.getCheckDataBalance()
            evaluationCheckInputCoverage = segregationPlotController.getCheckInputCoverage()
            if evaluationCheckInputCoverage == "no coverage":
                # if the coverage is not satisfied the process has to start from the beginning
                segregationPlotController.set_evaluation_check_data_balance("checking")
                segregationPlotController.set_evaluation_check_input_coverage("checking")
                evaluationCheckDataBalance = "checking"
                evaluationCheckInputCoverage = "checking"

        if serviceFlag is True or evaluationCheckDataBalance != "ok":
            # loop until I receive enough prepared session
            print("Receiving data...")
            # storageController.remove_all()

            while storageController.count() < limitPreparedSession:
                pass
                # the storage controller will retrive the data from the messageBus and will store into the db

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
                if evaluationCheckinputCoverage == "no":
                    continue

        if serviceFlag is True or (evaluationCheckDataBalance == "ok" and evaluationCheckInputCoverage == "ok"):
            # TODO i have to normalize data?
            # storageController.normalizeData()

            # here the human have checked that the data are correctly balanced
            # generate the learningSet
            learningSetGenerator = LearningSetGenerator(configParameter.getPercentageTrainingSplit(),
                                                        configParameter.getPercentageTestSplit(),
                                                        configParameter.getPercentageValidationSplit(),
                                                        storageController)
            learningSetGenerator.generateLearningSet()
            print("Learning set generated")


            sender = SegregationSystemSender(learningSetGenerator)

            sender.send_to_development()
            c=1
            #storageController.remove_all()  # remove the sessions

            # reset the evaluation in report files
            segregationPlotController.set_evaluation_check_data_balance("checking")
            segregationPlotController.set_evaluation_check_input_coverage("checking")

            # FIXME just for debug
            x = input('Do you want to continue: [Yes|No]')
            if "No" in x:
                break


if __name__ == "__main__":
    run()

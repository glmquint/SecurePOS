# takes data from the model
# gives info to the view
# ask the view to plot

from CheckInputCoverageModel import *
from CheckInputCoverageView import *
from CheckDataBalancingModel import *
from CheckDataBalancingView import *


class SegregationPlotController:

    def __init__(self, storageController, checkDataBalanceTolerance):
        self.__storageController = storageController
        self.__checkDataBalancingModel = CheckDataBalancingModel(storageController)
        self.__checkDataBalancingView = CheckDataBalanceView(checkDataBalanceTolerance)
        self.__checkInputCoverageModel = CheckInputCoverageModel(storageController)
        self.__checkInputCoverageView = CheckInputCoverageView()

    def plotDataBalance(self):
        # retrive data from the model
        preparedSession = self.__checkDataBalancingModel.retrivePreparedSession()
        # pass data to the view to plot
        self.__checkDataBalancingView.plotCheckDataBalance(preparedSession)

    def plotCheckInputCoverage(self):
        # retrive data from the model
        preparedSession = self.__checkInputCoverageModel.retrivePreparedSession()
        # pass data to the view to plot
        self.__checkInputCoverageView.plotCheckinputCoverageView(preparedSession)

    def getSimulatedCheckDataBalance(self):
        self.__checkDataBalancingView.getSimulatedCheckDataBalance()

    def getCheckDataBalance(self):
        self.__checkDataBalancingView.getCheckDataBalance()

    def getSimulatedCheckInputCoverage(self):
        self.__checkInputCoverageView.getSimulatedCheckInputCoverage()

    def getCheckInputCoverage(self):
        self.__checkInputCoverageView.getCheckInputCoverage()

    def setEvaluationCheckDataBalance(self, state):
        with open('Data/checkDataBalanceReport.json', 'w') as f:
            json.dump({"evaluation": state}, f)
            f.close()

    def setEvaluationCheckInputCoverage(self, state):
        with open('Data/checkInputCoverageReport.json', 'w') as f:
            json.dump({"evaluation": state}, f)
            f.close()

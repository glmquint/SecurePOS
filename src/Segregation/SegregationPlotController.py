from CheckInputCoverageModel import *
from CheckInputCoverageView import *
from CheckDataBalancingModel import *
from CheckDataBalancingView import *


class SegregationPlotController:

    def __init__(self, storageController, checkDataBalanceTolerance):
        self.__storageController = storageController
        self.__checkDataBalancingModel = CheckDataBalancingModel(storageController)
        self.__checkDataBalancingView = CheckDataBalanceView(checkDataBalanceTolerance,self.__checkDataBalancingModel)
        self.__checkInputCoverageModel = CheckInputCoverageModel(storageController)
        self.__checkInputCoverageView = CheckInputCoverageView(self.__checkInputCoverageModel)

    def plotDataBalance(self):
        # retrieve data from the model
        self.__checkDataBalancingModel.retrivePreparedSession()
        # pass data to the view to plot
        self.__checkDataBalancingView.plotCheckDataBalance()

    def plotCheckInputCoverage(self):
        # retrieve data from the model
        self.__checkInputCoverageModel.retrievePreparedSession()
        # pass data to the view to plot
        self.__checkInputCoverageView.plotCheckInputCoverageView()

    def getSimulatedCheckDataBalance(self):
        return self.__checkDataBalancingView.getSimulatedCheckDataBalance()

    def getCheckDataBalance(self):
        return self.__checkDataBalancingView.getCheckDataBalance()

    def getSimulatedCheckInputCoverage(self):
        return self.__checkInputCoverageView.getSimulatedCheckInputCoverage()

    def getCheckInputCoverage(self):
        return self.__checkInputCoverageView.getCheckInputCoverage()

    def setEvaluationCheckDataBalance(self, state):
        try:
            with open('Data/checkDataBalanceReport.json', 'w') as f:
                json.dump({"evaluation": state}, f)
                f.close()
        except Exception as e:
            print(e)

    def setEvaluationCheckInputCoverage(self, state):
        try:
            with open('Data/checkInputCoverageReport.json', 'w') as f:
                json.dump({"evaluation": state}, f)
                f.close()
        except Exception as e:
            print(e)


#takes data from the model
#gives info to the view
#ask the view to plot

from CheckInputCoverageModel import *
from CheckInputCoverageView import *
from CheckDataBalancingModel import *
from CheckDataBalancingView import *

class SegregationPlotController:

    def __init__(self):
        self.checkDataBalancingModel = CheckDataBalancingModel()
        self.checkDataBalancingView = CheckDataBalanceView()
        self.checkInputCoverageModel = CheckInputCoverageModel()
        self.checkInputCoverageView = CheckInputCoverageView()

    def plotDataBalance(self):
        # retrive data from the model
        preparedSession = self.checkDataBalancingModel.retrivePreparedSession()
        # pass data to the view to plot
        self.checkDataBalancingView.plotCheckDataBalance(preparedSession)

    def plotCheckInputCoverage(self):
        # retrive data from the model
        preparedSession = self.checkInputCoverageModel.retrivePreparedSession()
        # pass data to the view to plot
        self.checkDataBalancingView.plotCheckDataBalance(preparedSession)




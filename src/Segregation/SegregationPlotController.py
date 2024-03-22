from src.Segregation.CheckInputCoverageView import *
from src.Segregation.CheckDataBalancingView import *


class SegregationPlotController:

    def __init__(self, storageController, checkDataBalanceTolerance):
        self.__storage_controller = storageController
        self.__check_data_balancing_model = CheckDataBalancingModel(storageController)
        self.__check_data_balancing_view = CheckDataBalanceView(checkDataBalanceTolerance, self.__check_data_balancing_model)
        self.__check_input_coverage_model = CheckInputCoverageModel(storageController)
        self.__check_input_coverage_view = CheckInputCoverageView(self.__check_input_coverage_model)

    def plot_data_balance(self):
        # retrieve data from the model
        self.__check_data_balancing_model.retrive_prepared_session()
        # pass data to the view to plot
        self.__check_data_balancing_view.plot_check_data_balance()

    def plot_check_input_coverage(self):
        # retrieve data from the model
        self.__check_input_coverage_model.retrieve_prepared_session()
        # pass data to the view to plot
        self.__check_input_coverage_view.plot_check_input_coverage_view()

    def get_simulated_check_data_balance(self):
        return self.__check_data_balancing_view.get_simulated_check_data_balance()

    def get_check_data_balance(self):
        return self.__check_data_balancing_view.get_check_data_balance()

    def get_simulated_check_input_coverage(self):
        return self.__check_input_coverage_view.get_simulated_check_input_coverage()

    def get_check_input_coverage(self):
        return self.__check_input_coverage_view.get_check_input_coverage()

    @staticmethod
    def set_evaluation_check_data_balance(state):
        try:
            with open('Data/checkDataBalanceReport.json', 'w') as f:
                json.dump({"evaluation": state}, f)
                f.close()
        except Exception as e:
            print(e)

    @staticmethod
    def set_evaluation_check_input_coverage(state):
        try:
            with open('Data/checkInputCoverageReport.json', 'w') as f:
                json.dump({"evaluation": state}, f)
                f.close()
        except Exception as e:
            print(e)


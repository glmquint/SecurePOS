from src.Segregation.CheckInputCoverageView import *
from src.Segregation.CheckDataBalancingView import *


class SegregationPlotController:
    """
        Controller class responsible for managing the plotting of data balance
        and input coverage checks.

        Attributes:
        __limit_prepared_session (int): The limit of prepared session data to retrieve.
        __storage_controller (StorageController): An instance of the storage controller
                                                  used for data retrieval.
        __check_data_balancing_model (CheckDataBalancingModel): An instance of the data balancing
                                                               model to retrieve and process
                                                               data balance information.
        __check_data_balancing_view (CheckDataBalanceView): An instance of the view class to
                                                           visualize data balance information.
        __check_input_coverage_model (CheckInputCoverageModel): An instance of the input coverage
                                                                model to retrieve and process
                                                                input coverage information.
        __check_input_coverage_view (CheckInputCoverageView): An instance of the view class to
                                                             visualize input coverage information.

        """

    def __init__(
            self,
            storage_controller,
            check_data_balance_tolerance,
            limit_prepared_session):
        self.__limit_prepared_session = limit_prepared_session
        self.__storage_controller = storage_controller
        self.__check_data_balancing_model = CheckDataBalancingModel(
            storage_controller)
        self.__check_data_balancing_view = CheckDataBalanceView(
            check_data_balance_tolerance, self.__check_data_balancing_model)
        self.__check_input_coverage_model = CheckInputCoverageModel(
            storage_controller)
        self.__check_input_coverage_view = CheckInputCoverageView(
            self.__check_input_coverage_model)

    def plot_data_balance(self):
        # retrieve data from the model
        self.__check_data_balancing_model.retrieve_prepared_session(
            self.__limit_prepared_session)
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
            with open(f'{os.path.dirname(__file__)}/Data/checkDataBalanceReport.json', 'w') as f:
                json.dump({"evaluation": state}, f)
                f.close()
        except Exception as e:
            print(e)

    @staticmethod
    def set_evaluation_check_input_coverage(state):
        try:
            with open(f'{os.path.dirname(__file__)}/Data/checkInputCoverageReport.json', 'w') as f:
                json.dump({"evaluation": state}, f)
                f.close()
        except Exception as e:
            print(e)

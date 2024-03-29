from src.Segregation.LearningSetGenerator import LearningSetGenerator
from src.Segregation.SegregationPlotController import SegregationPlotController
from src.Segregation.SegregationSystemReceiver import PreparedSessionReceiver
from src.Segregation.SegregationSystemConfig import SegregationSystemConfig
from src.Segregation.SegregationSystemSender import SegregationSystemSender
from src.Storage.StorageController import StorageController
from src.DataObjects.Session import PreparedSession


class SegregationSystemOrchestrator:

    def __init__(self, config: SegregationSystemConfig = None):
        # get config parameter
        if not config:
            config = SegregationSystemConfig()
        self.config_parameter = config
        self.service_flag = self.config_parameter.get_service_flag()
        self.limit_prepared_session = self.config_parameter.get_sufficient_session_number()

        # instantiate database
        self.storage_controller = StorageController(
            {'name': 'PreparedSessionsDataStore', 'table_name': 'PreparedSessions'},
            PreparedSession)
        self.segregation_plot_controller = SegregationPlotController(
            self.storage_controller,
            self.config_parameter.get_tolerance_data_balancing(),
            self.limit_prepared_session)
        # instantiate and run receiver
        self.prepared_session_receiver = PreparedSessionReceiver(
            self.storage_controller,
            self.config_parameter.get_segregation_system_port(),
            self.config_parameter.get_segregation_system_endpoint())

        self.learning_set_generator = LearningSetGenerator(
            self.config_parameter.get_percentage_training_split(),
            self.config_parameter.get_percentage_test_split(),
            self.config_parameter.get_percentage_validation_split(),
            self.storage_controller,
            self.limit_prepared_session)

        self.sender = SegregationSystemSender(
            self.config_parameter, self.learning_set_generator)

    def run(self):
        # the server starts to run
        self.prepared_session_receiver.run()

        while True:

            evaluation_check_data_balance = ""
            evaluation_check_input_coverage = ""
            # the serviceFlag is false if the simplified stop and go
            # interaction is not active
            print(f"[{self.__class__.__name__}]: Server started")

            if not self.service_flag:
                # the value that can be assigned to the following two variable
                # is ( checking | ok | not balanced )
                evaluation_check_data_balance = self.segregation_plot_controller.get_check_data_balance()
                evaluation_check_input_coverage = self.segregation_plot_controller.get_check_input_coverage()
                if evaluation_check_input_coverage == "no coverage":
                    # if the coverage is not satisfied the process has to start
                    # from the beginning
                    self.segregation_plot_controller.set_evaluation_check_data_balance(
                        "checking")
                    self.segregation_plot_controller.set_evaluation_check_input_coverage(
                        "checking")
                    evaluation_check_data_balance = "checking"
                    evaluation_check_input_coverage = "checking"

            if self.service_flag or evaluation_check_data_balance != "ok":
                # loop until I receive enough prepared session
                print(f"[{self.__class__.__name__}]: Receiving data...")

                while self.storage_controller.count() < self.limit_prepared_session:
                    # the storage controller will retrive the data from the
                    # messageBus and will store into the db
                    pass

                print("Data correctly stored")

                # plot the graph
                self.segregation_plot_controller.plot_data_balance()
                print("Check data balance correctly plotted")

                if not self.service_flag:
                    break
                else:  # simulate the decision of the human
                    evaluation_data_balance_check = self.segregation_plot_controller.get_simulated_check_data_balance()
                    if evaluation_data_balance_check == "not performed":  # the test will not pass with a probability of 90%
                        # "data not balanced"
                        self.sender.send_to_messaging()
                        continue

            if self.service_flag or (
                    evaluation_check_data_balance == "ok" and evaluation_check_input_coverage != "ok"):
                # here the human have checked that the data are correctly
                # balanced

                # plot the checkInputCoverage graph
                self.segregation_plot_controller.plot_check_input_coverage()
                print("Check input coverage correctly plotted")

                # let's check input coverage
                if not self.service_flag:
                    break
                else:
                    evaluation_checkinput_coverage = self.segregation_plot_controller.get_simulated_check_input_coverage()
                    # "input not covered"
                    if evaluation_checkinput_coverage == "no":
                        self.sender.send_to_messaging()
                        continue

            if self.service_flag or (
                    evaluation_check_data_balance == "ok" and evaluation_check_input_coverage == "ok"):
                # storageController.normalizeData()

                # here the human have checked that the data are correctly balanced
                # generate the learningSet

                self.learning_set_generator.generate_learning_set()
                print("Learning set generated")

                self.sender.send_to_development()

                self.storage_controller.remove_all()  # remove the sessions

                # reset the evaluation in report files
                self.segregation_plot_controller.set_evaluation_check_data_balance(
                    "checking")
                self.segregation_plot_controller.set_evaluation_check_input_coverage(
                    "checking")


if __name__ == "__main__":
    segregation_system_orchestrator = SegregationSystemOrchestrator()
    segregation_system_orchestrator.run()

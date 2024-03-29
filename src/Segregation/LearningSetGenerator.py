import pandas as pd
from src.DataObjects.LearningSet import LearningSet
import math
from src.DataObjects.Session import PreparedSession


class LearningSetGenerator:
    """
    Class responsible for generating learning sets from prepared sessions.

    Attributes:
    __train_percentage (float): Percentage of data to be used for training.
    __test_percentage (float): Percentage of data to be used for testing.
    __validation_percentage (float): Percentage of data to be used for validation.
    __storage_controller (StorageController): An instance of the storage controller.
    __limit_prepared_session (int): The limit of prepared sessions to retrieve.
    learning_set (LearningSet): The generated learning set.

    Methods:
    generate_learning_set():
        Generates the learning set based on the specified percentages and storage controller.
    """

    def __init__(
            self,
            train_percentage,
            test_percentage,
            validation_percentage,
            storage_controller,
            limit_prepared_session):
        """
        Initializes the LearningSetGenerator with the given parameters.

        Parameters:
        train_percentage (float): Percentage of data to be used for training.
        test_percentage (float): Percentage of data to be used for testing.
        validation_percentage (float): Percentage of data to be used for validation.
        storage_controller (StorageController): An instance of the storage controller.
        limit_prepared_session (int): The limit of prepared sessions to retrieve.
        """
        self.__train_percentage = train_percentage
        self.__test_percentage = test_percentage
        self.__validation_percentage = validation_percentage
        self.__storage_controller = storage_controller
        self.__limit_prepared_session = limit_prepared_session
        self.leaning_set = None

    def generate_learning_set(self):
        """
        Generates the learning set based on the specified percentages and storage controller.
        """
        prepared_session_array: [PreparedSession] = self.__storage_controller.retrieve_n(
            self.__limit_prepared_session, True)

        # Get the cardinality of the prepared session
        cardinality_prepared_session = len(prepared_session_array)
        assert len(
            prepared_session_array) == cardinality_prepared_session, f"got unexpected cardinality for prepared session: {cardinality_prepared_session} instead of {len(prepared_session_array)}"

        # Calculate train, test, and validation set cardinalities
        test_set_cardinality = math.ceil(cardinality_prepared_session * self.__test_percentage)
        val_set_cardinality = math.ceil(cardinality_prepared_session * self.__validation_percentage)
        training_set_cardinality = cardinality_prepared_session - test_set_cardinality - val_set_cardinality

        # Split the dataset into train, test, and validation sets
        training_set = prepared_session_array[:training_set_cardinality]
        validation_set = prepared_session_array[
                         training_set_cardinality: training_set_cardinality + test_set_cardinality]
        test_set = prepared_session_array[training_set_cardinality + test_set_cardinality:]

        # Prepare the dictionaries to be converted into dataframes
        cols = training_set[0].to_json().keys() - {'uuid'}
        training_set_array = {col: [v.to_json()[col] for v in training_set] for col in cols}
        validation_set_array = {col: [v.to_json()[col] for v in validation_set] for col in cols}
        test_set_array = {col: [v.to_json()[col] for v in test_set] for col in cols}

        # Target labels are stored in a separate array
        training_set_label = training_set_array.pop('label')
        validation_set_label = validation_set_array.pop('label')
        test_set_label = test_set_array.pop('label')

        # Convert into named dataframes
        training_set_array = pd.DataFrame(training_set_array)
        validation_set_array = pd.DataFrame(validation_set_array)
        test_set_array = pd.DataFrame(test_set_array)

        dic = {
            'trainingSet': training_set_array,
            'validationSet': validation_set_array,
            'testSet': test_set_array,
            'trainingSetLabel': training_set_label,
            'validationSetLabel': validation_set_label,
            'testSetLabel': test_set_label
        }

        learning_set = LearningSet(dic, False)
        self.leaning_set = learning_set

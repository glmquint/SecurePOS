import pandas as pd
from src.DataObjects.LearningSet import LearningSet
import math
from src.DataObjects.Session import PreparedSession


class LearningSetGenerator:

    def __init__(
            self,
            train_percentage,
            test_percentage,
            validation_percentage,
            storage_controller,
            limit_prepared_session):
        self.__train_percentage = train_percentage
        self.__test_percentage = test_percentage
        self.__validation_percentage = validation_percentage
        self.__storage_controller = storage_controller
        self.__limit_prepared_session = limit_prepared_session
        self.leaning_set = None

    def generate_learning_set(self):
        prepared_session_array: [PreparedSession] = self.__storage_controller.retrieve_n(
            self.__limit_prepared_session, True)
        # sessions while we are processing the current ones
        cardinality_prepared_session = len(prepared_session_array)
        assert len(
            prepared_session_array) == cardinality_prepared_session, f"got unexpected cardinality for prepared session: {cardinality_prepared_session} instead of {len(prepared_session_array)}"

        # calculate train, test and validation splits
        test_set_cardinality = math.ceil(
            cardinality_prepared_session *
            self.__test_percentage)
        val_set_cardinality = math.ceil(
            cardinality_prepared_session *
            self.__validation_percentage)
        training_set_cardinality = cardinality_prepared_session - \
            test_set_cardinality - val_set_cardinality

        # split the dataset into train, test and validation
        training_set = prepared_session_array[:training_set_cardinality]
        validation_set = prepared_session_array[training_set_cardinality:
                                             training_set_cardinality + test_set_cardinality]
        test_set = prepared_session_array[training_set_cardinality +
                                       test_set_cardinality:]

        # prepare the dictionaries to be converted into dataframes
        cols = training_set[0].to_json().keys() - {'uuid'}
        training_set_array = dict(zip(cols, [0] * len(cols)))
        validation_set_array = dict(zip(cols, [0] * len(cols)))
        test_set_array = dict(zip(cols, [0] * len(cols)))
        for col in cols:
            training_set_array[col] = [v.to_json()[col] for v in training_set]
            validation_set_array[col] = [v.to_json()[col] for v in validation_set]
            test_set_array[col] = [v.to_json()[col] for v in test_set]

        # target labels are stored on a separate array
        training_set_label = training_set_array.pop('label')
        validation_set_label = validation_set_array.pop('label')
        test_set_label = test_set_array.pop('label')

        # convert into named dataframes
        training_set_array = pd.DataFrame(training_set_array)
        validation_set_array = pd.DataFrame(validation_set_array)
        test_set_array = pd.DataFrame(test_set_array)

        dic = dict()
        dic['trainingSet'] = training_set_array
        dic['validationSet'] = validation_set_array
        dic['testSet'] = test_set_array
        dic['trainingSetLabel'] = training_set_label
        dic['validationSetLabel'] = validation_set_label
        dic['testSetLabel'] = test_set_label

        learning_set = LearningSet(dic, False)

        self.leaning_set = learning_set

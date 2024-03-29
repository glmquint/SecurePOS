import pandas as pd
from src.DataObjects.Session import PreparedSession


class CheckInputCoverageModel:
    def __init__(self, storageController):
        self.__storageController = storageController
        self.__preparedSessionDF: pd.DataFrame = None

    def retrieve_prepared_session(self):
        self.__preparedSessionDF = self.data_normalized(
            self.__storageController.retrieve_all(False))

    def get_prepared_session_df(self) -> [PreparedSession]:
        return self.__preparedSessionDF

    @staticmethod
    def data_normalized(preparedSessions: [PreparedSession]) -> pd.DataFrame:
        columns = preparedSessions[0].to_json().keys() - {'label', 'uuid'}
        values = {
            attr: [
                ps.__dict__.get(
                    attr,
                    None) for ps in preparedSessions] for attr in columns}

        dataframe_data = pd.DataFrame(values)

        for column in dataframe_data.columns:
            if column == 'median_longitude':
                dataframe_data[column] += 180
            if column == 'median_latitude':
                dataframe_data[column] += 90
            dataframe_data[column] = (dataframe_data[column] - dataframe_data[column].min()) /\
                                     (dataframe_data[column].max() - dataframe_data[column].min())

        return dataframe_data

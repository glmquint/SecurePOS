import pandas as pd
from src.DataObjects.Session import PreparedSession


class CheckInputCoverageModel:
    def __init__(self, storage_controller):
        self.__storage_controller = storage_controller
        self.__prepared_session_df: pd.DataFrame = None

    def retrieve_prepared_session(self):
        self.__prepared_session_df = self.data_normalized(
            self.__storage_controller.retrieve_all(False))

    def get_prepared_session_df(self) -> [PreparedSession]:
        return self.__prepared_session_df

    @staticmethod
    def data_normalized(prepared_sessions: [PreparedSession]) -> pd.DataFrame:
        columns = prepared_sessions[0].to_json().keys() - {'label', 'uuid'}
        values = {
            attr: [
                ps.__dict__.get(
                    attr,
                    None) for ps in prepared_sessions] for attr in columns}

        dataframe_data = pd.DataFrame(values)

        for column in dataframe_data.columns:
            if column == 'median_longitude':
                dataframe_data[column] += 180
            if column == 'median_latitude':
                dataframe_data[column] += 90
            dataframe_data[column] = dataframe_data[column] / \
                dataframe_data[column].abs().max()

        return dataframe_data

import pandas as pd
from src.DataObjects.PreparedSession import PreparedSession


class CheckInputCoverageModel:
    def __init__(self, storageController):
        self.__storageController = storageController
        self.__preparedSessionList = None

    def retrieve_prepared_session(self):
        self.__preparedSessionList = self.data_normalized(self.__storageController.retrieve_all(False))

    def get_prepared_session_list(self):
        return self.__preparedSessionList

    @staticmethod
    def data_normalized(preparedSessions):
        tmp = []
        for p in preparedSessions:
            tmp.append(p.returnArray()[:len(p.returnArray()) - 1])

        dataframe_data = pd.DataFrame(tmp)

        df_max_scaled = dataframe_data.copy()
        for column in df_max_scaled.columns:
            if column == 2:
                df_max_scaled[column] += 180
            if column == 3:
                df_max_scaled[column] += 90
            df_max_scaled[column] = df_max_scaled[column] / df_max_scaled[column].abs().max()

        # print dataframe data
        prepared_sessions_list = []
        for index, row in df_max_scaled.iterrows():
            array = row.to_list()
            array.append("")
            prepared_sessions_list.append(PreparedSession(array))

        return prepared_sessions_list


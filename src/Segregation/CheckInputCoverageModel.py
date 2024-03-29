import pandas as pd
from src.DataObjects.Session import PreparedSession


class CheckInputCoverageModel:
    """
    Model class responsible for handling data related to input coverage checks.

    Attributes:
    __storage_controller (StorageController): An instance of the storage controller
                                              used for data retrieval.
    __prepared_session_df (pd.DataFrame): A DataFrame to store normalized prepared session data.

    Methods:
    retrieve_prepared_session():
        Retrieves all prepared sessions from the storage controller and normalizes the data.
    get_prepared_session_df() -> pd.DataFrame:
        Returns the normalized prepared session data as a DataFrame.
    data_normalized(prepared_sessions: [PreparedSession]) -> pd.DataFrame:
        Normalizes the prepared session data and returns it as a DataFrame.
    """

    def __init__(self, storage_controller):
        """
        Initializes the CheckInputCoverageModel with the given storage controller.

        Parameters:
        storage_controller (StorageController): The storage controller to use for data retrieval.
        """
        self.__storage_controller = storage_controller
        self.__prepared_session_df: pd.DataFrame = None

    def retrieve_prepared_session(self):
        """
        Retrieves all prepared sessions from the storage controller and normalizes the data.
        """
        self.__prepared_session_df = self.data_normalized(
            self.__storage_controller.retrieve_all(False))

    def get_prepared_session_df(self) -> pd.DataFrame:
        """
        Returns the normalized prepared session data as a DataFrame.

        Returns:
        pd.DataFrame: The normalized prepared session data.
        """
        return self.__prepared_session_df

    @staticmethod
    def data_normalized(prepared_sessions: [PreparedSession]) -> pd.DataFrame:
        """
        Normalizes the prepared session data and returns it as a DataFrame.

        Parameters:
        prepared_sessions ([PreparedSession]): A list of prepared session objects.

        Returns:
        pd.DataFrame: The normalized prepared session data.
        """
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
            dataframe_data[column] = (dataframe_data[column] - dataframe_data[column].min()) /\
                                     (dataframe_data[column].max() - dataframe_data[column].min())

        return dataframe_data

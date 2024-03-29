import os
import pandas as pd
from src.Development.Testing import TestReportModel


class TestReportView:
    """
    A class used to view the test report in the development system.

    Attributes
    ----------
    path_to_save : str
        The path where the test report will be saved.
    model : TestReportModel
        The model of the test report.

    Methods
    -------
    __init__(self, filename: str, test_report_model: TestReportModel)
        Initializes the TestReportView class with the filename and the test report model.
    update(self)
        Updates the test report view by saving the current state of the test report model to a CSV file.
    """
    # class implementation...class TestReportView:
    path_to_save: str = None
    model: TestReportModel = None

    def __init__(self, filename: str, test_report_model: TestReportModel):
        self.path_to_save = f'{os.path.dirname(__file__)}/{filename}.csv'
        self.model = test_report_model

    def update(self):
        if os.path.exists(self.path_to_save):
            os.remove(self.path_to_save)
        df = pd.DataFrame(self.model.to_dict(), index=[0])
        df.to_csv(self.path_to_save, index=False)

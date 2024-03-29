import os

from src.Development.Testing import TestReportModel
import pandas as pd


class TestReportView:
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

from src.Development.Testing import TestReportModel
import pandas as pd


class TestReportView:
    path_to_save: str = None
    model: TestReportModel = None

    def __init__(self, filename: str, test_report_model: TestReportModel):
        self.path_to_save = f'src/Development/{filename}.csv'
        self.model = test_report_model

    def update(self):
        df = pd.DataFrame(self.model.to_dict())
        df.to_csv(self.path_to_save, index=False)
        print(f'Test report saved to {self.path_to_save}')

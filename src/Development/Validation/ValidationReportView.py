from src.Development.Validation import ValidationReportModel
import pandas as pd


class ValidationReportView:
    path_to_save: str = None
    model: ValidationReportModel = None

    def __init__(self, filename: str, test_report_model: ValidationReportModel):
        self.path_to_save = f'src/Development/{filename}.csv'
        self.model = test_report_model

    def update(self):
        df = pd.DataFrame(self.model.to_dict())
        df.to_csv(self.path_to_save, index=False)
        print(f'Validation report saved to {self.path_to_save}')

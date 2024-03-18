import os

from src.Development.Validation import ValidationReportModel
import pandas as pd


class ValidationReportView:
    path_to_save: str = None
    model: ValidationReportModel = None

    def __init__(self, path: str, validation_report_model: ValidationReportModel):
        self.path_to_save = f'{path}/Validation_Report.csv'
        self.model = validation_report_model

    def update(self):
        if os.path.exists(self.path_to_save):
            os.remove(self.path_to_save)
        df = pd.DataFrame(self.model.to_dict())
        df.to_csv(self.path_to_save, index=False)
        print(f'Validation report saved to {self.path_to_save}')

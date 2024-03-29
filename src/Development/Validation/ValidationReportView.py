import os
import pandas as pd
from src.Development.Validation import ValidationReportModel


class ValidationReportView:
    """
    A class used to view the validation report in the development system.

    Attributes
    ----------
    path_to_save : str
        The path where the validation report will be saved.
    model : ValidationReportModel
        The model of the validation report.

    Methods
    -------
    __init__(self, path: str, validation_report_model: ValidationReportModel)
        Initializes the ValidationReportView class with a path and a validation report model.
    update(self)
        Updates the validation report view by saving the model to a CSV file.
    """
    # class implementation...class ValidationReportView:
    path_to_save: str = None
    model: ValidationReportModel = None

    def __init__(
            self,
            path: str,
            validation_report_model: ValidationReportModel):
        self.path_to_save = f'{path}/Validation_Report.csv'
        self.model = validation_report_model

    def update(self):
        if os.path.exists(self.path_to_save):
            os.remove(self.path_to_save)
        df = pd.DataFrame(self.model.to_dict())
        df.to_csv(self.path_to_save, index=False)
        print(f'Validation report saved to {self.path_to_save}')

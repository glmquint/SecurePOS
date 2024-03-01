from src.Development import ValidationReportModel

class ValidationReportView:
    path_to_save: str = None
    model: ValidationReportModel = None

    def __init__(self, filename: str, test_report_model: ValidationReportModel):
        self.path_to_save = f'src/Development/{filename}.png'
        self.model = test_report_model

    def update(self):
        # TODO: implement the figure update using the model
        pass

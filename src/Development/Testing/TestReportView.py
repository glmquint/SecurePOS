from src.Development.Testing import TestReportModel


class TestReportView:
    path_to_save: str = None
    model: TestReportModel = None

    def __init__(self, filename: str, test_report_model: TestReportModel):
        self.path_to_save = f'src/Development/{filename}.png'
        self.model = test_report_model

    def update(self):
        # TODO: implement the figure update using the model
        pass

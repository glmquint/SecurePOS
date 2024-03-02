class EvaluationReportModel:
    def __init__(self):
        self.TotalErrorTollerated = 5
        self.ConsecutiveErrorTollerated = 2
        self.labels = []
        self.TotalError = 0
        self.ConsecutiveError = 0

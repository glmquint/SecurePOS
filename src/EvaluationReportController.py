from src.EvaluationReportModel import EvaluationReportModel
from src.EvaluationReportViewer import EvaluationReportViewer


class EvaluationReportController:
    evaluation = EvaluationReportModel()
    reportviewer = EvaluationReportViewer()

    def generatereport(self, labels, securitylabels):
        consecutiverror = 0
        totalerror = 0
        consecutive = False
        for x in range(0, len(labels)):
            if labels[x] != securitylabels[x]:
                if not consecutive:
                    consecutive = True
                consecutiverror = consecutiverror + 1
                totalerror = totalerror + 1
            else:
                consecutive = False
                consecutiverror = 0
        self.evaluation.TotalError = totalerror
        self.evaluation.ConsecutiveError = consecutiverror
        self.evaluation.labels = labels
        self.reportviewer.update(self.evaluation)
        return

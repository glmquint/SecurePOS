class EvaluationReportViewer:
    result = ""

    def update(self, evaluationreportmodel):
        print(
            "Total error:" + evaluationreportmodel.TotalError + ",Max error tollerated:" + evaluationreportmodel.TotalErrorTollerated)
        print(
            "Total consecutive error:" + evaluationreportmodel.ConsecutiveError + ", Max consecutive error tollerated:" + evaluationreportmodel.ConsecutiveErrorTollerated)
        return

    def getResult(self):
        print(
            "Say Yes to confirm, No to decline:"
        )
        input(self.result)
        return

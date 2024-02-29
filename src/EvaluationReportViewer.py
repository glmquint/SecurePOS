class EvaluationReportViewer:
    result = ""

    def update(self, evaluationreportmodel):
        print(
            "Total error:" + evaluationreportmodel.TotalError + ",Max error tollerated:" + evaluationreportmodel.TotalErrorTollerated)
        print(
            "Total consecutive error:" + evaluationreportmodel.ConsecutiveError + ", Max consecutive error tollerated:" + evaluationreportmodel.ConsecutiveErrorTollerated)
        return

    def getresult(self):

        while True:
            print(
                "Please write Yes to confirm, No to decline:"
            )
            input(self.result)
            self.result = self.result.lower()
            if self.result != "yes" or self.result != "no":
                print(
                    "Answer not accepted, retry.\n"
                )
            else:
                print("Answer accepted.")
                break
        return

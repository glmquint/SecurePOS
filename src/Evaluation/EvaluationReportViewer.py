class EvaluationReportViewer:

    def __init__(self):
        self.result = ""

    def update(self, evaluationreportmodel):
        print(
            f'Total error: {evaluationreportmodel.TotalError},Max error tollerated: {evaluationreportmodel.TotalErrorTollerated}'
        )
        print(
            f'Total consecutive error: {evaluationreportmodel.ConsecutiveError}, Max consecutive error tollerated:{evaluationreportmodel.ConsecutiveErrorTollerated}'
        )
        self.getresult()
        return

    def getresult(self):

        while True:
            self.result = input("Please write Yes to confirm, No to decline, esc to leave:")
            self.result = self.result.lower()
            if self.result == "esc":
                exit()
            if self.result == "yes":
                print("Classifier accepted.")
                break
            if self.result == "no":
                print("Classifier rejected.")
                break
        return

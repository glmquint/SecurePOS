from random import randint

from src.Evaluation.EvaluationReportModel import EvaluationReportModel
from src.Evaluation.EvaluationReportViewer import EvaluationReportViewer


class EvaluationReportController:

    def __init__(self):
        self.evaluationmodel = EvaluationReportModel()
        self.reportviewer = EvaluationReportViewer()
        self.result = False

    def update(self):
        self.evaluationmodel.generatereport()
        #self.reportviewer.print(self.evaluationmodel.labels[0],self.evaluationmodel[1])
        self.evaluationmodel.removelabels()
        return

    def getresult(self,human_simulate = False):

        if not human_simulate:
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
        else:
            print("Simulating human operator...")
            if randint(0,10) > 5:
                self.result="yes"
                print("Classifier accepted.")
            else:
                self.result="no"
                print("Classifier rejected.")
        print("Evaluation phase done.")
        return

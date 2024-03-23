import json
import os
from random import randint

from src.Evaluation.EvaluationReportModel import EvaluationReportModel
from src.Evaluation.EvaluationReportViewer import EvaluationReportViewer
from src.JsonIO.JsonValidator import JSONValidator



class EvaluationReportController:

    def __init__(self,config):
        self.evaluationmodel = EvaluationReportModel(config)
        self.reportviewer = EvaluationReportViewer()
        self.result = False

    def update(self):
        self.evaluationmodel.generatereport()
        self.reportviewer.print(self.evaluationmodel,self.evaluationmodel.tick_array)
        self.evaluationmodel.removelabels()
        return

    def getresult(self,human_simulate = False):

        if not human_simulate:
            validator = JSONValidator(f"{os.path.dirname(__file__)}/./../DataObjects/Schema/action.json")
            action_json = open(f"{os.path.dirname(__file__)}/data/action.json")
            action = json.load(action_json)
            validator.validate_data(action)
            self.result = action["action"]
            # while True:
            #     self.result = input("Please write Yes to confirm, No to decline, esc to leave:")
            #     self.result = self.result.lower()
            #     if self.result == "esc":
            #         print("Closing...")
            #         self.evaluationmodel.sufficient_label_number = -1
            #         self.evaluationmodel.removelabels()
            #         exit()
            if self.result == "confirm":
                print("Classifier accepted.")
            else:
                print("Classifier rejected.")
        else:
            print("Simulating human operator...")
            if randint(0,10) > 5:
                self.result="confirm"
                print("Classifier accepted.")
            else:
                self.result="reject"
                print("Classifier rejected.")
        print("Evaluation phase done.")
        return

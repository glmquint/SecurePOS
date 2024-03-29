"""This module handles the ReportModel and ReportViewer"""
import json
import os
from random import randint

from src.Evaluation.EvaluationReportModel import EvaluationReportModel
from src.Evaluation.EvaluationReportViewer import EvaluationReportViewer
from src.JsonIO.JsonValidator import JSONValidator


class EvaluationReportController:
    """This is the main class of the report controller"""

    def __init__(self, config):
        self.evaluation_model = EvaluationReportModel(config)
        self.report_viewer = EvaluationReportViewer()
        self.result = False

    def update(self):
        """the main function, it will generate report,
        save the result in the .png and will remove the evaluate labels"""
        self.evaluation_model.generate_report()
        self.report_viewer.save_evaluation_result(
            self.evaluation_model, self.evaluation_model.tick_array)
        self.evaluation_model.remove_labels()

    def getresult(self, human_simulate=False):
        """this function read the json file to retrieve the human choice"""
        if not human_simulate:
            validator = JSONValidator(
                f"{os.path.dirname(__file__)}/./../DataObjects/Schema/action.json")
            with open(f"{os.path.dirname(__file__)}/data/action.json", encoding="utf-8")\
                    as action_json:
                action = json.load(action_json)
                validator.validate_data(action)
                self.result = action["action"]
                if self.result == "confirm":
                    print("Classifier accepted.")
                else:
                    print("Classifier rejected.")
        else:
            print("Simulating human operator...")
            if randint(0, 10) > 5:
                self.result = "confirm"
                print("Classifier accepted.")
            else:
                self.result = "reject"
                print("Classifier rejected.")
        print("Evaluation phase done.")

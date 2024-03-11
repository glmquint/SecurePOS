from src.DataObjects.AttackRiskLabel import AttackRiskLabel
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig


class EvaluationReportModel:
    def __init__(self):
        self.TotalErrorTollerated = 5
        self.TotalError = 0
        self.ConsecutiveErrorTollerated = 2
        self.ConsecutiveError = 0
        self.scontroller_label = StorageController(DBConfig("evaluation", "labels", "label", ),
                                                   type(AttackRiskLabel(None)))
        self.scontroller_security = StorageController(DBConfig("evaluation", "security_labels", "label"),
                                                      type(AttackRiskLabel(None)))
        self.labels = self.retrieve()


    def retrieve(self):
        labels = self.scontroller_label.retrieve_all()
        slabels = self.scontroller_security.retrieve_all()
        return [labels, slabels]


    def removelabels(self):
        self.scontroller_security.remove_all()
        self.scontroller_label.remove_all()

    def generatereport(self):
        labels = self.labels[0]
        security_labels = self.labels[1]
        #assert len(labels) == len(securitylabels)
        consecutiverror = 0
        totalerror = 0
        consecutive = False
        for x in range(0, len(labels)):
            if labels[x] != security_labels[x]:
                if not consecutive:
                    consecutive = True
                consecutiverror = consecutiverror + 1
                totalerror = totalerror + 1
            else:
                consecutive = False
                consecutiverror = 0
        self.TotalError = totalerror
        self.ConsecutiveError = consecutiverror
        return

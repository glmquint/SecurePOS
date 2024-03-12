from src.DataObjects.AttackRiskLabel import AttackRiskLabel
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig


class EvaluationReportModel:
    def __init__(self,number):
        self.TotalErrorTollerated = 5
        self.TotalError = 0
        self.ConsecutiveErrorTollerated = 2
        self.ConsecutiveError = 0
        self.scontroller_label = StorageController(DBConfig("evaluation", "labels", "label", ),
                                                   type(AttackRiskLabel(None)))
        self.scontroller_security = StorageController(DBConfig("evaluation", "security_labels", "label"),
                                                      type(AttackRiskLabel(None)))
        self.sufficient_label_number = number
        self.labels = self.retrieve()


    def retrieve(self):
        labels = self.scontroller_label.retrieve(self.sufficient_label_number)
        slabels = self.scontroller_security.retrieve(self.sufficient_label_number)
        return [labels, slabels]


    def removelabels(self):
        self.scontroller_security.remove(self.sufficient_label_number)
        self.scontroller_label.remove(self.sufficient_label_number)

    def generatereport(self):
        self.labels = self.retrieve()
        labels = self.labels[0]
        security_labels = self.labels[1]
        consecutiverror = 0
        totalerror = 0
        consecutive = False
        for x in range(0, len(labels)):
            if labels[x].attackRiskLabel[1] != security_labels[x].attackRiskLabel[1] :
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

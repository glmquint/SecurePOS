from src.DataObjects.AttackRiskLabel import AttackRiskLabel
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig


class EvaluationReportModel:
    def __init__(self,config):
        self.TotalErrorTollerated = config.tollerated_error
        self.TotalError = 0
        self.ConsecutiveErrorTollerated = config.tollerated_consecutive_error
        self.ConsecutiveError = 0
        self.tick_array = []
        self.scontroller_label = StorageController(DBConfig("evaluation", "labels"),
                                                   type(AttackRiskLabel(None)))
        self.scontroller_security = StorageController(DBConfig("evaluation", "security_labels"),
                                                      type(AttackRiskLabel(None)))
        self.sufficient_label_number = config.sufficient_label_number
        self.labels = self.retrieve()



    def retrieve(self):
        labels = self.scontroller_label.retrieveAll()
        slabels = self.scontroller_security.retrieveAll()
        return [labels, slabels]


    def removelabels(self):
        self.scontroller_security.removeAll()
        self.scontroller_label.removeAll()

    def generatereport(self):
        self.labels = self.retrieve()
        self.tick_array.clear()
        labels = self.labels[0]
        security_labels = self.labels[1]
        consecutiverror = 0
        totalerror = 0
        consecutive = False
        maxconsecutive = 0
        for x in range(0, len(labels)):
            if labels[x].attackRiskLabel[1] != security_labels[x].attackRiskLabel[1] :
                totalerror = totalerror + 1
                self.tick_array.append("X")
                if not consecutive:
                    consecutive = True
                    if consecutive == 0:
                        consecutiverror = 1
                    else:
                        consecutiverror = consecutiverror + 1
                else:
                    consecutiverror = consecutiverror + 1
            else:
                self.tick_array.append("V")
                consecutive = False
                maxconsecutive= max(consecutiverror,maxconsecutive)
                consecutiverror = 0
        self.TotalError = totalerror
        self.ConsecutiveError = maxconsecutive
        return

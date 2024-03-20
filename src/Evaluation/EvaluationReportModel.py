from src.DataObjects.AttackRiskLabel import AttackRiskLabel
from src.DataObjects.Record import Label
from src.Storage.StorageController import StorageController
from src.Storage.dbConfig import DBConfig


class EvaluationReportModel:
    def __init__(self,config):
        self.TotalErrorTollerated = config.tollerated_error
        self.TotalError = 0
        self.ConsecutiveErrorTollerated = config.tollerated_consecutive_error
        self.ConsecutiveError = 0
        self.tick_array = []
        self.scontroller_label = StorageController({'name': 'evaluation', 'table_name': 'labels'},type(Label()))
        #self.scontroller_label = StorageController(DBConfig("evaluation", "labels"),
                                                   #type(Label()))
        self.scontroller_security = StorageController({'name': 'evaluation', 'table_name': 'security_labels'},type(Label()))
        #self.scontroller_security = StorageController(DBConfig("evaluation", "security_labels"),
        self.sufficient_label_number = config.sufficient_label_number
        self.labels = []
        #self.labels = self.retrieve()



    def retrieve(self):
        labels = self.scontroller_label.retrieve_all()
        slabels = self.scontroller_security.retrieve_all()
        return [labels, slabels]


    def removelabels(self):
        self.scontroller_security.remove_all()
        self.scontroller_label.remove_all()

    def check_valid_labels(self):
        a = self.labels[0]
        b = self.labels[1]
        intersection = [value.uuid for value in [x for x in a] if value.label not in [y.label for y in [x for x in b]]]
        if not intersection:
            print("Labels and Security Labels are not matching.Aborting.")
            exit()
        return
    def generatereport(self):
        self.labels = self.retrieve()
        self.tick_array.clear()
        self.check_valid_labels()
        labels = self.labels[0]
        security_labels = self.labels[1]
        consecutiverror = 0
        totalerror = 0
        consecutive = False
        maxconsecutive = 0
        for x in range(0, len(labels)):
            if labels[x].label[1] != security_labels[x].label[1]:
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

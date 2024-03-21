from random import randint

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
        x = {x.uuid for x in self.labels[0]}
        y = {x.uuid for x in self.labels[1]}
        #print(x.difference(y))
        #print([(x.label,x.uuid) for x in a])
        #print([(x.label,x.uuid) for x in b])
        #difference = [value.uuid for value in [x for x in a] if value.uuid not in [y.uuid for y in [x for x in b]]]
        #print(difference)
        difference = ([uid for uid in x.difference(y)],[uid for uid in y.difference(x)])
        if len(difference[0]) != 0 or len(difference[1]) != 0:
            print(difference)
            print("Labels and Security Labels are not matching.Aborting.")
            self.removelabels()
            exit()
        return

    def sort_labels(self):
        self.labels[0].sort(key= lambda x:x.uuid)
        self.labels[1].sort(key= lambda x:x.uuid)

    def generatereport(self):
        self.labels = self.retrieve()
        self.tick_array.clear()
        self.check_valid_labels()
        self.sort_labels()
        labels = self.labels[0]
        security_labels = self.labels[1]
        consecutiverror = 0
        totalerror = 0
        consecutive = False
        maxconsecutive = 0
        for x in range(0, len(labels)):
            if labels[x].label != security_labels[x].label:
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

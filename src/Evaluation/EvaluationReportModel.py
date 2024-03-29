"""This module is used to display the result in a png."""
from src.DataObjects.Record import Label
from src.Storage.StorageController import StorageController


class EvaluationReportModel:
    """this is the main class of the report model."""

    def __init__(self, config):
        self.total_error_tollerated = config.tollerated_error
        self.total_error = 0
        self.consecutive_error_tollerated = config.tollerated_consecutive_error
        self.consecutive_error = 0
        self.tick_array = []
        self.scontroller_label = StorageController(
            {'name': 'evaluation', 'table_name': 'labels'}, type(Label()))
        self.scontroller_security = StorageController(
            {'name': 'evaluation', 'table_name': 'security_labels'}, type(Label()))
        self.sufficient_label_number = config.sufficient_label_number
        self.labels = []

    def retrieve(self):
        """this function retrieve n labels from db"""
        retrieve = self.scontroller_label.retrieve_n_labels(
            self.sufficient_label_number)
        return [retrieve[0], retrieve[1]]

    def remove_labels(self):
        """SQLITE has a trigger to delete the security labels."""
        self.scontroller_label.remove_joined_labels(
            self.sufficient_label_number)

    def check_valid_labels(self):
        """this function checks that the labels retrieve are matching"""
        x_label = {x_label.uuid for x_label in self.labels[0]}
        y_label = {x_label.uuid for x_label in self.labels[1]}
        difference = ([uid for uid in x_label.difference(y_label)],
                          [uid for uid in y_label.difference(x_label)])
        if len(difference[0]) != 0 or len(difference[1]) != 0:
            print(difference)
            print("Labels and Security Labels are not matching.Aborting.")
            self.remove_labels()
            raise Exception("Labels and Security Labels are not matching.")

    def sort_labels(self):
        """this function just sort labels"""
        self.labels[0].sort(key=lambda x: x.uuid)
        self.labels[1].sort(key=lambda x: x.uuid)

    def generate_report(self):
        """this function evaluate the error"""
        self.labels = self.retrieve()
        self.tick_array.clear()
        self.check_valid_labels()
        self.sort_labels()
        labels = self.labels[0]
        security_labels = self.labels[1]
        consecutive_error = 0
        total_error = 0
        consecutive = False
        max_consecutive = 0
        for x_iterator in range(0, len(labels)):
            if labels[x_iterator].label != security_labels[x_iterator].label:
                total_error = total_error + 1
                self.tick_array.append("X")
                if not consecutive:
                    consecutive = True
                consecutive_error = consecutive_error + 1
                max_consecutive = max(consecutive_error, max_consecutive)
            else:
                self.tick_array.append("V")
                consecutive = False
                max_consecutive = max(consecutive_error, max_consecutive)
                consecutive_error = 0
        self.total_error = total_error
        self.consecutive_error = max_consecutive

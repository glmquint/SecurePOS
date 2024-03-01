from src.Development.ValidationRow import ValidationRow
from src.Storage.StorageController import StorageController


class ValidationReportView:
    validation_rows: [ValidationRow] = None

    def __init__(self, storage_controller: StorageController):
        rows = storage_controller.retrieve_all()
        for row in rows:
            self.validation_rows.append(ValidationRow(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))


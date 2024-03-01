from src.Development.TestRow import TestRow
from src.Storage.StorageController import StorageController


class TestReportView:
    rows : [TestRow] = None

    def __init__(self, storage_controller: StorageController):
        rows = storage_controller.retrieve_all()
        for row in rows:
            self.rows.append(TestRow(row[0], row[1], row[2], row[3]))
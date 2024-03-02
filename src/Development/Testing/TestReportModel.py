from src.Development.Testing.TestRow import TestRow


class TestReportView:
    rows: [TestRow] = None

    def __init__(self, from_tuples: [tuple]):
        for row in from_tuples:
            self.rows.append(TestRow(row[0], row[1], row[2], row[3]))

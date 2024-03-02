from src.Development.Validation.ValidationRow import ValidationRow


class ValidationReportView:
    validation_rows: [ValidationRow] = None

    def __init__(self, from_tuples: [tuple]):
        for row in from_tuples:
            self.validation_rows.append(ValidationRow(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))


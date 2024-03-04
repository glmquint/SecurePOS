from src.Development.Validation.ValidationRow import ValidationRow


class ValidationReportModel:
    validation_rows: [ValidationRow] = None

    def __init__(self, from_tuples: [tuple]):
        for row in from_tuples:
            self.validation_rows.append(ValidationRow(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    def to_dict(self):
        return [row.to_dict() for row in self.validation_rows]
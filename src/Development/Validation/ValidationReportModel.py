from src.Development.Training.Scoreboard import Scoreboard
from src.Development.Validation.ValidationRow import ValidationRow


class ValidationReportModel:
    """
    A class used to model the validation report in the development system.

    Attributes
    ----------
    validation_rows : list of ValidationRow
        The rows of the validation report.

    Methods
    -------
    __init__(self, scoreboard: Scoreboard)
        Initializes the ValidationReportModel class with a scoreboard.
    to_dict(self)
        Converts the validation rows to a dictionary format.
    """
    # class implementation...class ValidationReportModel:
    validation_rows: [ValidationRow] = None

    def __init__(self, scoreboard: Scoreboard):
        self.validation_rows = []
        for i in range(len(scoreboard.mse)):
            self.validation_rows.append(
                ValidationRow(
                    scoreboard.classifiers[i].name,
                    scoreboard.mse[i],
                    scoreboard.validation_error[i],
                    scoreboard.train_error[i],
                    scoreboard.classifiers[i].number_of_layers,
                    scoreboard.classifiers[i].number_of_neurons))

    def to_dict(self):
        return [row.to_dict() for row in self.validation_rows]

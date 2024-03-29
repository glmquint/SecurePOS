import bisect
from src.DataObjects.Classifier import Classifier


class Scoreboard:
    """
    A class used to manage a scoreboard of classifiers in the development system.

    Attributes
    ----------
    classifiers : list
        The list of classifiers.
    mse : list
        The list of Mean Squared Errors corresponding to each classifier.
    train_error : list
        The list of training errors corresponding to each classifier.
    validation_error : list
        The list of validation errors corresponding to each classifier.
    limit : int
        The maximum number of classifiers that can be stored in the scoreboard.

    Methods
    -------
    __init__(self, limit: int)
        Initializes the Scoreboard class with a limit on the number of classifiers.
    insert_classifier(self, classifier: Classifier, mse: float, train_error: float, validation_error: float)
        Inserts a classifier into the scoreboard, maintaining the order of classifiers based on the Mean Squared Error.
    """
    # class implementation...class Scoreboard:
    classifiers: [Classifier] = None
    mse: [float] = None
    train_error: [float] = None
    validation_error: [float] = None
    limit: int = None

    def __init__(self, limit: int):
        self.limit = limit
        self.classifiers = []
        self.mse = []
        self.train_error = []
        self.validation_error = []

    def insert_classifier(
            self,
            classifier: Classifier,
            mse: float,
            train_error: float,
            validation_error: float):
        index = bisect.bisect(self.mse, mse)
        if len(self.mse) < self.limit:
            self.mse.insert(index, mse)
            self.train_error.insert(index, train_error)
            self.validation_error.insert(index, validation_error)
            self.classifiers.insert(index, classifier)
        else:
            if index < self.limit:
                self.mse.pop()
                self.classifiers.pop()
                self.train_error.pop()
                self.validation_error.pop()
                self.mse.insert(index, mse)
                self.train_error.insert(index, train_error)
                self.validation_error.insert(index, validation_error)
                self.classifiers.insert(index, classifier)

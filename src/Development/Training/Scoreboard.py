from src.Development import Classifier
import bisect


class Scoreboard:
    classifiers: [Classifier] = None
    mse: [float] = None
    limit: int = None
    train_error: [float] = None
    validation_error: [float] = None

    def __init__(self, limit: int):
        self.limit = limit

    def insert_classifier(self, classifier: Classifier, mse: float, train_error: float, validation_error: float):
        index = bisect.bisect(self.mse, mse)
        if index < self.limit:
            self.mse.insert(index, mse)
            self.train_error.insert(index, train_error)
            self.validation_error.insert(index, validation_error)
            classifier.save_model(f"models/{index}.sav")
            self.classifiers.insert(index, classifier)
            self.mse.pop()
            self.classifiers.pop()

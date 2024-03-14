import os

from src.Development import Classifier
import bisect


class Scoreboard:
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

    def save_classifiers(self, path: str):
        for i in range(len(self.mse)):
            self.classifiers[i].save_model(path)

    def remove_classifiers(self):
        for i in range(len(self.mse)):
            filename = f'classifiers/{self.classifiers[i].name}.sav'
            if os.path.exists(filename):
                os.remove(filename)

    def insert_classifier(self, classifier: Classifier, mse: float, train_error: float, validation_error: float):
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

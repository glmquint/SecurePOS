class ClassifierTest:
    def __init__(self, classifier):
        self.classifier = classifier

    def getClassifier(self):
        return self.classifier
    def to_json(self):
        return {
            "classifier": self.classifier
        }
    def __str__(self):
        return f"Classifier: {self.classifier}"
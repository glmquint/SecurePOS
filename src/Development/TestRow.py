class TestRow:
    classifier_name: str = None
    validation_error: float = None
    testing_error: float = None
    generalization_tolerance: float = None
    
    def __init__(self, classifier_name: str, validation_error: float, testing_error: float, generalization_tolerance: float):
        self.classifier_name = classifier_name
        self.validation_error = validation_error
        self.testing_error = testing_error
        self.generalization_tolerance = generalization_tolerance
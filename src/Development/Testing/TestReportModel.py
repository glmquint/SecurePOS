class TestReportModel:
    """
    A class used to model the test report in the development system.

    Attributes
    ----------
    classifier_name : str
        The name of the classifier.
    validation_error : float
        The validation error of the classifier.
    testing_error : float
        The testing error of the classifier.
    generalization_tolerance : float
        The generalization tolerance of the classifier.

    Methods
    -------
    __init__(self, classifier_name: str, validation_error: float, testing_error: float, generalization_tolerance: float)
        Initializes the TestReportModel class with the classifier name, validation error, testing error, and generalization tolerance.
    to_dict(self)
        Converts the TestReportModel instance to a dictionary.
    """
    # class implementation...class TestReportModel:
    classifier_name: str = None
    validation_error: float = None
    testing_error: float = None
    generalization_tolerance: float = None

    def __init__(
            self,
            classifier_name: str,
            validation_error: float,
            testing_error: float,
            generalization_tolerance: float):
        self.classifier_name = classifier_name
        self.validation_error = validation_error
        self.testing_error = testing_error
        self.generalization_tolerance = generalization_tolerance

    def to_dict(self):
        return {
            'classifier_name': self.classifier_name,
            'validation_error': self.validation_error,
            'testing_error': self.testing_error,
            'generalization_tolerance': self.generalization_tolerance}

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from src.Development.Classifier import Classifier
from src.Development.Training.HyperParameterLimit import HyperParameterLimit
from src.Storage.StorageController import StorageController


class TrainProcess:
    number_of_iterations: int = None
    classifier: Classifier = None
    grid_search: GridSearchCV = None
    hyperparameters: HyperParameterLimit = None
    avg_hyperparameters: dict = None

    def set_average_hyperparameters(self):
        avg_hyperparameters = {}
        for key in self.hyperparameters.dict_hyperparameters.keys():
            avg_hyperparameters[key] = (self.hyperparameters.dict_hyperparameters[key][0] +
                                        self.hyperparameters.dict_hyperparameters[key][1]) / 2

    def set_number_of_iterations(self, number_of_iterations: int):
        self.number_of_iterations = number_of_iterations

    def __init__(self, hyperparameters: HyperParameterLimit,storage_controller: StorageController):
        self.storage_controller = storage_controller
        self.hyperparameters = hyperparameters

    def train(self):
        self.classifier = Classifier(self.avg_hyperparameters['number_of_neurons'],
                                     self.avg_hyperparameters['number_of_layers'])
        self.grid_search = GridSearchCV(self.classifier.model, self.avg_hyperparameters)
        self.grid_search.fit(learning_set, learning_set_labels)

    def save_learning_result (self):
        best_model = self.grid_search.best_estimator_
        best_loss_values = best_model.loss_curve_
        dbconf = DBConfig('training', 'learning_plot')
        storage_controller = StorageController(dbconf, type(LearningPlotModel((0, 0, 0)))
        storage_controller.save(LearningPlotModel(best_loss_values))



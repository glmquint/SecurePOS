class HyperParameterLimit:
    dict_hyperparameters: dict

    def __init__(self):
        pass

    def add_hyperparameter(self, name: str, min: int, max: int, step: int):
        self.dict_hyperparameters[name] = (min, max, step)

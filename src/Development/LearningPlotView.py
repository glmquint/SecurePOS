class LearningPlotView:

    def __init__(self, parent, model):
        self._model = model
        self._parent = parent


    def update(self):
        self._parent.plot(self._model.get_data())

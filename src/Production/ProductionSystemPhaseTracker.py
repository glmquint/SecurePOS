# A class for tracking the phase of the production system and the time spent in each phase

class ProductionSystemPhaseTracker:
    def __init__(self, production_window, evaluation_window):
        self.production_window = production_window
        self.evaluation_window = evaluation_window
        self.system_counter = 0
        self.is_production = True
    #
    def increseCounter(self):
        self.system_counter += 1
        self.system_counter %= (self.production_window + self.evaluation_window)
        self.is_production = self.system_counter < self.production_window
    def isProduction(self):
        return self.is_production
    # A print function for the phase tracker
    def __str__(self):
        return f"Production Window: {self.production_window},\nEvaluation Window: {self.evaluation_window},\n" \
               f"System Counter: {self.system_counter},\nIs Production: {self.is_production}"
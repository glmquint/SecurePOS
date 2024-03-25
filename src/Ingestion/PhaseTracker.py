class PhaseTracker:
    def __init__(self, config):
        self.config = config
        self.count = 0
    pass

    def increment(self):
        self.count += 1
        self.count %= self.config['production_phase_duration'] + self.config['evaluation_phase_duration']

    def isEvalPhase(self):
        return self.count >= self.config['production_phase_duration'] and self.config['phase'] == "Production"

    def isDevPhase(self):
        return self.config['phase'] == "Development"

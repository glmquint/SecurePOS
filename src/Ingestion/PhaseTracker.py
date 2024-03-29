class PhaseTracker:
    """
    This class is responsible for tracking the phase of the ingestion and production process.

    The PhaseTracker class maintains a count and uses a configuration to determine the current phase.
    It provides methods to increment the count and check if the system is in the evaluation or development phase.

    Attributes:
        config (dict): Configuration for the phase tracker.
        count (int): A counter used to track the phase.

    Methods:
        increment(): Increments the count and wraps it around based on the phase durations.
        isEvalPhase(): Checks if the system is in the evaluation phase.
        isDevPhase(): Checks if the system is in the development phase.
    """

    def __init__(self, config):
        self.config = config
        self.count = 0

    def increment(self):
        self.count += 1
        self.count %= self.config['production_phase_duration'] + \
            self.config['evaluation_phase_duration']

    def isEvalPhase(self):
        return self.count >= self.config['production_phase_duration'] and self.config['phase'] == "Production"

    def isDevPhase(self):
        return self.config['phase'] == "Development"

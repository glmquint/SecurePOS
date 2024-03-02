class DevelopmentSystemConfigurations:
    ip: str
    port: int
    hyperparameters: dict

    def __init__(self, ip: str, port: int, hyperparameters: dict):
        self.ip = ip
        self.port = port
        self.hyperparameters = hyperparameters

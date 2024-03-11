class ServiceMessage:
    __system = None
    __content = None

    def __init__(self, dict):
        self.__dict__ = dict

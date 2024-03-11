class Message:
    __system = None
    __timestamp = None
    __label = None # this can be start/end/intermidiate

    def __init__(self, dict):
        self.__dict__ = dict


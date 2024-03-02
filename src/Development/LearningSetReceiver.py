from src.MessageBus.MessageBus import MessageBus
from src.JsonIO.JSONEndpoint import JSONEndpoint

class LearningSetReceiver:
    learning_set = None
    message_bus_ref = None
    def __init__(self, message_bus:MessageBus):
        self.message_bus_ref = message_bus

    def receiveLearningSet(self):
        # TODO: Implement the recv
        learning_set = JSONEndpoint()
        self.learning_set = learning_set
        self.message_bus_ref.addTopic("LearningSet")
        self.message_bus_ref.pushTopic("LearningSet", learning_set)
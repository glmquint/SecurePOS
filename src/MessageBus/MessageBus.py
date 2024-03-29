import queue


class MessageBus:
    """
        This class is responsible for managing a message bus system. It initializes the message bus with
        a list of topics, and provides methods to push to a topic, pop from a topic, and add a new topic.

        Attributes:
            messageQueues: A dictionary where the keys are the topics and the values are queue.Queue objects.

        Methods:
            pushTopic: Pushes a value to a specific topic.
            popTopic: Pops a value from a specific topic.
            addTopic: Adds a new topic to the message bus.
    """
    def __init__(self, topics=list()):
        self.messageQueues = dict()
        for t in topics:
            self.messageQueues[t] = queue.Queue()

    def pushTopic(self, topic, val):
        # if the topic do not exists return
        if topic not in self.messageQueues.keys():
            return
        q = self.messageQueues.get(topic)
        q.put(val)
        return

    def popTopic(self, topic):
        if topic not in self.messageQueues.keys():
            raise ValueError("Topic not found")
        return self.messageQueues[topic].get()

    def addTopic(self, topic):
        # check
        if topic not in self.messageQueues.keys():
            self.messageQueues[topic] = queue.Queue()


# same testing
if __name__ == "__main__":
    msg = MessageBus(["b", "c"])
    msg.addTopic("a")
    msg.pushTopic("a", 2)
    msg.pushTopic("a", 3)
    print(msg.popTopic("a"))
    print(msg.popTopic("a"))
    print(msg.popTopic("a"))  # would block

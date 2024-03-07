import queue


class MessageBus:
    messageQueues = dict()

    def __init__(self, topics):
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
        return self.messageQueues[topic].get()

    def addTopic(self, topic):
        # check
        if topic not in self.messageQueues.keys():
            self.messageQueues[topic] = queue.Queue()


# same testing
#msg = MessageBus(["b", "c"])
#msg.addTopic("a")
#msg.pushTopic("a", 2)
#msg.pushTopic("a", 3)
#print(msg.popTopic("a"))
#print(msg.popTopic("a"))
#print(msg.popTopic("a")) # would block
#

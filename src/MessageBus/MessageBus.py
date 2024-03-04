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
        q = self.messageQueues.get(topic)
        # if the queue is empty return "empty"
        if q.qsize() == 0:
            return "empty"
        else:
            val = q.get()
            return val

    def addTopic(self, topic):
        # check
        if topic not in self.messageQueues.keys():
            self.messageQueues[topic] = queue.Queue()


# same testing
msg = MessageBus(["b", "c"])
#msg.pushTopic("b",9)
print(msg.popTopic("b"))
msg.addTopic("a")
msg.pushTopic("a", 2)
msg.pushTopic("a", 3)
print(msg.popTopic("a"))
print(msg.popTopic("a"))
print(msg.popTopic("a"))

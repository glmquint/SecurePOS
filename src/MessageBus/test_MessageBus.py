from unittest import TestCase
import threading
import time

from src.MessageBus.MessageBus import MessageBus


class TestMessageBus(TestCase):
    def test_general(self):
        msg = MessageBus(["b", "c"])
        msg.addTopic("a")
        msg.pushTopic("a", 2)
        msg.pushTopic("a", 3)
        assert msg.popTopic("a") == 2
        assert msg.popTopic("a") == 3

        # Define a function for the secondary thread to pop from the topic
        def pop_topic():
            time.sleep(1)  # Wait for some time
            popped_value = msg.popTopic("a")
            print("Popped value in secondary thread:", popped_value)

        # Create and start the secondary thread
        secondary_thread = threading.Thread(target=pop_topic)
        secondary_thread.start()

        # Wait for a while to check if the secondary thread is blocked
        time.sleep(2)

        # Assert if the secondary thread is still alive, meaning it's blocked
        self.assertTrue(
            secondary_thread.is_alive(),
            "Secondary thread is already dead")
        msg.pushTopic("a", 4)
